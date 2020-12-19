def test_player_from_api_response():
    """
    Test data fetching and instantiating Player from API response.

    Tests whether
        > data can be fetched successfully from the Riot API `GET getLeagueEntries` endpoint,
        > a `Player` object can be successfully converted from this raw API response.
    """
    from .player import Player
    from utils.enums import RankedQueue, Server, Tier, Division
    import os
    from riotwatcher import LolWatcher

    watcher = LolWatcher(os.environ.get("X_RIOT_TOKEN"))
    server = Server.EUW.value
    resp = watcher.league.entries(
        region=server,
        queue=RankedQueue.SOLO_DUO.value,
        tier=Tier.GOLD.value,
        division=Division.FOUR.value,
        page=1,
    )
    # check if request was successful, and if there is any data at all
    assert resp is not None and len(resp) > 0

    single_obj = resp[0]
    single_obj["server"] = Server.EUW
    player = Player._from_api_dict(league_entry_DTO=single_obj)
    # player instance should be successfully instantiated
    assert player is not None
