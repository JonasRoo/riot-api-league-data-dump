def test_ranked_distribution():
    from .rank_distributions import TotalDistribution as TotalRankedDistribution

    assert TotalRankedDistribution is not None
    assert 0.97 <= (sum([d.total for d in TotalRankedDistribution])) <= 1.0


def test_server_distribution():
    from .server_distributions import TotalDistribution as TotalServerDistribution
    from ..enums import Server

    for field in Server:
        # for every defined server, we want to have a figure
        assert hasattr(TotalServerDistribution, field.name)

    assert sum([getattr(TotalServerDistribution, field.name) for field in Server]) == 1
