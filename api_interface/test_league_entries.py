def test_correct_fetching():
    import os
    from riotwatcher import LolWatcher
    from .league_entries import _TESTING_PURPOSES_EF

    api_key = os.environ.get("X_RIOT_TOKEN")
    assert api_key is not None
    lolwatcher = LolWatcher(api_key=api_key)
    from utils.enums import RankedQueue, Server, Tier, Division

    for idx, data in enumerate(_TESTING_PURPOSES_EF):
        assert idx < 1
        assert data is not None