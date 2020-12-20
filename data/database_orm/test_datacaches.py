from nose.tools import with_setup
import os


def _setup_in_memory_db():
    """
    Setup for any database-related tests to avoid collision with production DB.
    """
    # with this flag, the database-interface will use an in-memory sqlite instance
    os.environ["RIOT_DB_TEST_ENV"] = "TESTING"


def _after_db_tests():
    """
    Teardown to remove env-variable that signals `testing` to the database-interface.
    """
    os.unsetenv("RIOT_DB_TEST_ENV")


@with_setup(setup=_setup_in_memory_db, teardown=_after_db_tests)
def test_database_cache():
    """
    Test the database cache by using a mock in-memory sqlite database.
    Temporarily enters TEST-mode for the application, but always exits it after.
    """
    from ..data_caches import DatabaseCache
    from ..database_orm.tables.player import Player
    from .session.session_handler import session_scope
    from api_interface.league_entries import EntryFetcher, _TESTING_PURPOSES_EF_PARAMS
    from riotwatcher import LolWatcher
    import math

    # delete all previous models for this test
    with session_scope() as session:
        session.query(Player).delete()

    with DatabaseCache(TableInstance=Player, batch_size=16) as cache:
        # slighty interference with another test here (`EntryFetcher` test), but should be fine
        ef = EntryFetcher(**_TESTING_PURPOSES_EF_PARAMS)
        for idx, entries in enumerate(ef):
            cache.add(entries)
    # check that the cache was saved and flushed in correct amount of batches
    assert cache.current_batch_no == math.ceil(ef.max_entries / cache.batch_size)
    assert cache.empty

    with session_scope() as session:
        players = session.query(Player).distinct(Player.summoner_id).all()
        # check whether DatabaseCache has correctly processed and added data to the database
        # (specifically checks DatabaseCache.save() function)
        assert players
        assert len(players) == ef.max_entries
