from typing import Mapping, Any, Optional, Generator, List
from .database_orm import bot_declarative_base
from .database_orm.session.session_handler import session_scope


class BaseDataCache:
    """
    A context manager for database caches to implement, to sequentially store and save data to any data interface.
    Provides basic functionality of 'caching' blocks of data (as Lists) as they come in.
    Data is then saved (optionally in chunks) as it is added to the cache.
    Subclasses need to implement the `save()` method! (interface to the data saving medium).

    Args:
        batch_size (Optional[int], optional): If provided, data is saved in chunks of size [batch_size]. Defaults to 0.
            > if set to 0 data is wholly saved whenever it's added to the cache.
    """

    def __init__(self, batch_size: Optional[int] = 0) -> None:
        """
        The 'cache' itself is the `data` field of the class.
        """
        self.batch_size = batch_size
        self.current_batch_no = 0
        self.data = []

    def add(self, new_data: List[Mapping[str, Any]]) -> None:
        """
        Interface to add new data to the cache.

        Args:
            new_data (List[Mapping[str, Any]]): [description]
        """
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
        """
        Chunks data into sizes of [batch_size] and yields whether chunks are full-sized or not.
        Chunks are stored in the `data` field.

        Yields:
            Generator[bool, None, None]: whether the chunk in `data` is full_sized (=batch_size).
        """
        # NOTE(jonas): we have redundance in here (albeit small) memory complexity is raised by `O(batch_size)`
        # this could maybe be implemented as a custom queue
        _total_data = self.data
        for i in range(0, len(_total_data), self.batch_size):
            # chunk our data into lists of size `batch_size`
            # and sequentially add them into the `data` field after each yield.
            self.data = _total_data[i : i + self.batch_size]
            # yield whether data holds a full-sized batch
            yield len(self.data) == self.batch_size
        del _total_data

    def flush(self) -> None:
        """
        Empties the cache.
        """
        self.current_batch_no += 1
        self.data = []

    def save(self) -> None:
        """
        Saves data in the cache to the underlying data medium.
        Needs to be implemented by subclasses!

        Raises:
            NotImplementedError: Needs to be implemented by subclasses!
        """
        raise NotImplementedError("This method needs to be implemented by subclass!")

    def save_and_flush(self):
        """
        Shortcut for subsequently calling `save()` and `flush()`
        """
        self.save()
        self.flush()

    def __enter__(self):
        """
        This is meant to be used as a context manager.
        """
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> Optional[bool]:
        """
        Caches are context manangers to ensure correct cleanup
            > e.g. when there's still some data left in the cache after iteration concluded.

        Args:
            *exc_type (exc): When the `exit` is invoked because of on out-of-context-scope error.


        Returns:
            Optional[bool]: False, if the context was exited because of an external error.
        """
        # on the last batch, save data even if we are below size
        if exc_type:
            return False

        self.save_and_flush()


class DatabaseCache(BaseDataCache):
    """
    Subclass of a Datacache that interfaces any SQLAlchemy declarative base.

    Args:
        TableInstance (bot_declarative_base): table_space that inherits from a declarative base.
    """

    def __init__(self, TableInstance: bot_declarative_base, *args, **kwargs) -> None:
        self.TableInstance = TableInstance
        # the method name on the TableInstance class that converts a raw API Dict-like response to an instance of the table.
        self._converter_field_name = "_from_api_dict"
        super().__init__(*args, **kwargs)

    def save(self):
        with session_scope() as session:
            # if we can map the Dict[] instances in our `data` field, use the converter method
            if hasattr(self.TableInstance, self._converter_field_name):
                instances = [
                    getattr(self.TableInstance, self._converter_field_name)(d) for d in self.data
                ]
            else:
                # if not, just try to instantiate it directly from the `data` fields
                instances = [self.TableInstance(**d) for d in self.data]

            # save them all to the table
            session.add_all(instances)
