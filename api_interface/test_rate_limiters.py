from .rate_limiters import RateLimiter, RateLimiterCollection
from typing import Tuple
import datetime


def _get_fresh_limiters() -> Tuple[RateLimiter]:
    return (
        RateLimiter(n_requests=2, per_interval="10seconds"),
        RateLimiter(n_requests=100, per_interval="20seconds"),
        RateLimiter(n_requests=5, per_interval="1minutes"),
    )


def test_initialization_of_rate_limiters():
    """
    Tests that rate limiters are initialized correctly
    """
    limiters = _get_fresh_limiters()
    for limiter in limiters:
        assert limiter.last_invoked == datetime.datetime.min
    rate_limiters = RateLimiterCollection(rate_limiters=limiters)
    assert rate_limiters.last_invoked == datetime.datetime.min


def test_rate_limiter_collection_does_not_want_to_wait_before_first_set():
    limiters = _get_fresh_limiters()
    rate_limiters = RateLimiterCollection(rate_limiters=limiters)
    assert rate_limiters.get_wait_time() is None


def test_rate_limiter_collection_after_set_wants_to_wait():
    limiters = _get_fresh_limiters()
    rate_limiters = RateLimiterCollection(rate_limiters=limiters)
    for idx in range(10):
        to_wait = rate_limiters.get_wait_time()
        rate_limiters.last_invoked = datetime.datetime.now()
        if idx != 0:
            assert to_wait is not None