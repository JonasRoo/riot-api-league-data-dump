def test_correct_fetching():
    import os
    from riotwatcher import LolWatcher
    from .league_entries import EntryFetcher, _TESTING_PURPOSES_EF_PARAMS

    api_key = os.environ.get("X_RIOT_TOKEN")
    assert api_key is not None
    lolwatcher = LolWatcher(api_key=api_key)
    from utils.enums import RankedQueue, Server, Tier, Division

    ef = EntryFetcher(**_TESTING_PURPOSES_EF_PARAMS)
    for idx, data in enumerate(ef):
        assert idx < 1
        assert data is not None