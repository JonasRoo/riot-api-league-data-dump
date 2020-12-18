from typing import Mapping
from ..enums import Server


class ServerDistribution:
    """
    The %age of players actively playing RANKED on a particular server.

    Args:
        server_distribution (Mapping[Server, int]): a mapping of {Server_Enum: total_ranked_player_population}
            > will be added as attrs to instance by the name of their enum (ServerDistribution.EUW, not ServerDistribution.Server.EUW)!
    """

    def __init__(self, server_distribution: Mapping[Server, int], **kwargs) -> None:
        self._total_population = sum(server_distribution.values())
        for k, v in server_distribution.items():
            setattr(self, k.name, v / self._total_population)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self) -> str:
        _fields = [s.name for s in Server if s.name in vars(self)]
        distributions = [f"{f}: {getattr(self, f):.2%}" for f in _fields]
        return f"ServerDistribution (total: {self._total_population:3,}): {{{' | '.join(distributions)}}}"


# source: https://www.reddit.com/r/leagueoflegends/comments/hbt6yq/server_by_ranked_population_2020_vs_2018/
TotalDistribution = ServerDistribution(
    server_distribution={
        # reduced significantly to reduce their presence in the dataset
        Server.KR: 3_878_509 // 100,
        Server.EUW: 3_112_127,
        Server.NA: 1_726_310,
        Server.EUNE: 1_560_010,
        Server.BR: 1_370_524,
        Server.TR: 820_695,
        Server.LAN: 689_731,
        Server.LAS: 688_672,
        Server.RU: 214_561,
        Server.OCE: 210_306,
        Server.JP: 115_552,
    }
)
