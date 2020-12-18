from typing import List, Dict, Any, Optional
import os
from riotwatcher import LolWatcher
from utils.enums import Tier, Division, RankedQueue, Server


class EntryFetcher:
    """
    Iterator class to progressively fetch more and more pages from the `getEntries` Riot API.

    Args:
        lolwatcher (LolWatcher): Instantiated lolwatcher.
        tier (Tier): Tier enum member (e.g. Tier.PLATINUM).
        division (Division): Division enum member (e.g. Division.FOUR).
        ranked_queue (RankedQueue): RankedQueue enum member (e.g. RankedQueue.RANKED_SOLO_DUO_5x5).
        server (Server): Server enum member (e.g. Server.EUW).
        max_entries (int, optional): Optional amount of max individual(!) entries to fetch before stopping iteration. Defaults to 0.
    """

    def __init__(
        self,
        lolwatcher: LolWatcher,
        tier: Tier,
        division: Division,
        ranked_queue: RankedQueue,
        server: Server,
        max_entries: Optional[int] = 0,
    ) -> None:
        """
        Initializes an iterable EndpointFetcher for the Riot `getEntries` LoL API.
        """
        self.lolwatcher = lolwatcher
        self.tier = tier
        self.division = division
        self.ranked_queue = ranked_queue
        self.server = server
        assert max_entries >= 0, f"`max_entries` cannot be below 0!"
        self.max_entries = max_entries
        self.current_page = 1
        self.entries_fetched = 0

    def fetch_next_page(self) -> List[Dict[str, Any]]:
        """
        Fetches data for `self.current_page` from Riot getEntries API.
        """
        return self.lolwatcher.league.entries(
            region=self.server.value,
            queue=self.ranked_queue.value,
            tier=self.tier.value,
            division=self.division.value,
            page=self.current_page,
        )

    def __iter__(self):
        """
        Entry point for iterator.
        """
        return self

    def __next__(self) -> List[Dict[str, Any]]:
        """
        Iterates and yields over entries in a given league / division / server.
        Iteration parameter := self.current_page

        Raises:
            StopIteration: there are 2 stop criteria for the iteration:
                > 1) there's no entries left for those params > can't fetch more
                > 2) max_entries we want to fetch has been exceeded

        Returns:
            List[Dict[str, Any]]: List of league entries.
        """
        if self.max_entries and self.entries_fetched >= self.max_entries:
            raise StopIteration
        data = self.fetch_next_page()
        if self.max_entries:
            data = data[: self.max_entries - self.entries_fetched]

        self.entries_fetched += len(data)
        self.current_page += 1

        return data


_TESTING_PURPOSES_EF = EntryFetcher(
    lolwatcher=LolWatcher(os.environ.get("X_RIOT_TOKEN")),
    tier=Tier.GOLD,
    division=Division.FOUR,
    ranked_queue=RankedQueue.SOLO_DUO,
    server=Server.EUW,
    max_entries=50,
)