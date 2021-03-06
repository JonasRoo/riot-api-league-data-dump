def test_correct_fetching():
    """
    Test EntryFetcher class fetching.
    """
    import os
    from .league_entries import EntryFetcher, _TESTING_PURPOSES_EF_PARAMS

    api_key = os.environ.get("X_RIOT_TOKEN")
    assert api_key is not None

    ef = EntryFetcher(**_TESTING_PURPOSES_EF_PARAMS)
    for idx, data in enumerate(ef):
        assert data is not None

    assert idx < 1