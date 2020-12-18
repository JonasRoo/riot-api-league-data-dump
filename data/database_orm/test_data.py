from nose.tools import with_setup
import os


def _setup_in_memory_db():
    os.environ["RIOT_DB_TEST_ENV"] = "TESTING"


def _after_db_tests():
    os.unsetenv("RIOT_DB_TEST_ENV")


@with_setup(_setup_in_memory_db, _after_db_tests)
def test_database_cache():
    from ..data_caches import DatabaseCache
    from ..database_orm.tables.player import Player
    from .session.session_handler import session_scope
    from api_interface.league_entries import EntryFetcher, _TESTING_PURPOSES_EF_PARAMS
    from riotwatcher import LolWatcher
    import math

    with DatabaseCache(TableInstance=Player, batch_size=16) as cache:
        ef = EntryFetcher(**_TESTING_PURPOSES_EF_PARAMS)
        for idx, entries in enumerate(ef):
            cache.add(entries)
    assert cache.current_batch_no == math.ceil(ef.max_entries / cache.batch_size)

    with session_scope() as session:
        players = session.query(Player).distinct(Player.summoner_id).all()
        assert players
        assert len(players) == ef.max_entries
