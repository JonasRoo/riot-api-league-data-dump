from typing import Iterable, Mapping
from utils.enums import Tier, Division


class _RankedDistribution:
    """
    The %age of players in a particular tier per each division (when applicable).

    Args:
        tier (Tier): The tier this distribution applies for
        division_distributions (Mapping[Division, float]): A mapping of {division: %age of playerbase in this division}
    """

    def __init__(self, tier: Tier, division_distribution: Mapping[Division, float]) -> None:
        self.tier = tier
        self.distribution = division_distribution
        self.total = sum(division_distribution.values())

    def __str__(self) -> str:
        distributions = [f"{div.value}: {perc:.2%}" for div, perc in self.distribution.items()]
        return f"{self.tier.value} ({self.total:.2%}): {{{' | '.join(distributions)}}}"


# =V------------ STATIC DISTRIBUTIONS ------------V
# source: https://www.leagueofgraphs.com/rankings/rank-distribution (as of 12/17/20)
# Q: why static distributions?
# A: %age distributions across servers is (mostly) neglilible in the non-challenger-esque leagues.

Diamond = _RankedDistribution(
    tier=Tier.DIAMOND,
    division_distribution={
        Division.ONE: 0.0014,
        Division.TWO: 0.0027,
        Division.THREE: 0.0050,
        Division.FOUR: 0.0150,
    },
)

Platinum = _RankedDistribution(
    tier=Tier.PLATINUM,
    division_distribution={
        Division.ONE: 0.013,
        Division.TWO: 0.013,
        Division.THREE: 0.021,
        Division.FOUR: 0.067,
    },
)

Gold = _RankedDistribution(
    tier=Tier.GOLD,
    division_distribution={
        Division.ONE: 0.029,
        Division.TWO: 0.051,
        Division.THREE: 0.068,
        Division.FOUR: 0.140,
    },
)

Silver = _RankedDistribution(
    tier=Tier.SILVER,
    division_distribution={
        Division.ONE: 0.059,
        Division.TWO: 0.085,
        Division.THREE: 0.073,
        Division.FOUR: 0.110,
    },
)

Bronze = _RankedDistribution(
    tier=Tier.BRONZE,
    division_distribution={
        Division.ONE: 0.070,
        Division.TWO: 0.059,
        Division.THREE: 0.031,
        Division.FOUR: 0.033,
    },
)

Iron = _RankedDistribution(
    tier=Tier.IRON,
    division_distribution={
        Division.ONE: 0.0160,
        Division.TWO: 0.0086,
        Division.THREE: 0.0050,
        Division.FOUR: 0.0019,
    },
)

# sum of all distributions, excluding challenger-esque tiers (challenger, grandmaster, master)
TotalDistribution = (
    Iron,
    Bronze,
    Silver,
    Gold,
    Platinum,
    Diamond,
)

if __name__ == "__main__":
    for d in TotalDistribution:
        print(d)