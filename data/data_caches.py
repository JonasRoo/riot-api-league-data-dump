from typing import Mapping, Any, Optional, Generator, List
from .database_orm import bot_declarative_base
from .database_orm.session.session_handler import session_scope


class BaseDataCache:
    def __init__(self, batch_size: Optional[int] = 0) -> None:
        self.batch_size = batch_size
        self.current_batch_no = 0
        self.data = []

    def add(self, new_data: List[Mapping[str, Any]]) -> None:
        self.data.extend(new_data)
        if not self.batch_size:
            # short circuit if no batch_size is defined
            self.save_and_flush()
            return

        for is_full_size_chunk in self.chunk_internally_and_is_fullsized():
            if is_full_size_chunk:
                # this is a fully-sized chunk > save it
                self.save_and_flush()
            else:
                # not a fully-sized batch > persist until next `add` call
                return

    def chunk_internally_and_is_fullsized(self) -> Generator[bool, None, None]:
        # NOTE(jonas): we have redundance in here (albeit small) memory complexity is raised by `O(batch_size)`
        # this could maybe be implemented as a custom queue
        _total_data = self.data
        for i in range(0, len(_total_data), self.batch_size):
            self.data = _total_data[i : i + self.batch_size]
            yield len(self.data) == self.batch_size
        _total_data = []

    def flush(self) -> None:
        self.current_batch_no += 1
        self.data = []

    def save(self) -> None:
        raise NotImplementedError("This method needs to be implemented by subclass!")

    def save_and_flush(self):
        self.save()
        self.flush()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> Optional[bool]:
        # on the last batch, save data even if we are below size
        if exc_type:
            return False

        self.save_and_flush()


class DatabaseCache(BaseDataCache):
    def __init__(self, TableInstance: bot_declarative_base, *args, **kwargs) -> None:
        self.TableInstance = TableInstance
        self._converter_field_name = "_from_api_dict"
        super().__init__(*args, **kwargs)

    def save(self):
        with session_scope() as session:
            if hasattr(self.TableInstance, self._converter_field_name):
                instances = [
                    getattr(self.TableInstance, self._converter_field_name)(d) for d in self.data
                ]
            else:
                instances = [self.TableInstance(**d) for d in self.data]

            session.add_all(instances)
