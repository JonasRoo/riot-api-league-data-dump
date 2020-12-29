from typing import Optional, Tuple, Iterable
import datetime


# NOTE(jonas): we might also want to have a "greedy" rate limiter
class RateLimiter:
    """
    A generic rate limiter for API-call-based workflows.
    Implements a `20 requests every 1 second`-type structure.
    Works in a non-greedy / spaced-out manner, meaning:
        > the n requests you have available per interval are evenly spaced out across it.
    This class does not assume that the user follows the wait-time,
    so the `last_invoked` property needs to be set manually when the call is made!

    Args:
        n_requests (int): the amount of requests you're allowed to make per a given interval
        per_interval (str): given restricting interval. Format: `1seconds`, `20minutes` etc.
    """

    def __init__(self, n_requests: int, per_interval: str) -> "RateLimiter":
        self._n_requests = n_requests
        self._per_interval = per_interval
        self.time, self.unit = self.parse_increments(increments=per_interval)
        self._last_invoked = datetime.datetime.min

    @property
    def last_invoked(self) -> datetime.datetime:
        """
        Property (with setter) describing when an API-call was last made.
        If this has never been manually set, it's just `datetime.datetime.min`.

        Returns:
            datetime.datetime: datetime object when last call was made.
        """
        return self._last_invoked

    @last_invoked.setter
    def last_invoked(self, new_last_invoked: datetime.datetime) -> None:
        """
        Use this when you actually make the call you're rate-limiting.
        Only sets this property when the new parameter is after the current one.

        Args:
            new_last_invoked (datetime.datetime): new timestamp to set to, typically time of API call.
        """
        if new_last_invoked > self._last_invoked:
            self._last_invoked = new_last_invoked

    def reset(self) -> None:
        """
        Resets the `last_invoked` property.
        """
        self._last_invoked = datetime.datetime.min

    @staticmethod
    def parse_increments(increments: str) -> Tuple[int, str]:
        """
        Parses a time increment string of form `{number}{unit(s)}.
        Example output:
            "2weeks" --> (2, "weeks")

        Args:
            increments (str): The string to extract (number, unit) from. NO WHITESPACE ALLOWED!

        Returns:
            Tuple[int, str]: (amount, unit)
        """
        number = int("".join([c for c in increments if c.isdigit()]))
        unit = "".join([c.lower() for c in increments if c.isalpha()])
        return number, unit

    def maybe_get_wait_duration(self) -> Optional[float]:
        """
        Calculates and returns whether user should wait before next call based on this limiter.

        Returns:
            Optional[float]: None, if shouldn't wait. time-to-wait in seconds, if should wait.
        """
        next_invoke_time = self._last_invoked + datetime.timedelta(**{self.unit: self.time})
        should_wait_for = (
            next_invoke_time - datetime.datetime.now()
        ).total_seconds() / self._n_requests
        if should_wait_for > 0.0:
            return should_wait_for


class RateLimiterCollection:
    """
    Helper class to store a collection of rate-limiters and easily calculate & manage wait-times.
    An example of this would be a given API-key with multiple rate limitations.

    Args:
        rate_limiters (Iterable[RateLimiter]): An iterable of `RateLimiter` to manage.
    """
    def __init__(self, rate_limiters: Iterable[RateLimiter]) -> None:
        self.rate_limiters = rate_limiters
        self._last_invoked = datetime.datetime.min

    @property
    def last_invoked(self) -> datetime.datetime:
        """
        Property (with setter) describing when an API-call was last made.
        If this has never been manually set, it's just `datetime.datetime.min`.

        Returns:
            datetime.datetime: datetime object when last call was made.
        """
        return self._last_invoked

    @last_invoked.setter
    def last_invoked(self, new_last_invoked: datetime.datetime) -> None:
        """
        Use this when you actually make the call you're rate-limiting. Sets across all member `RateLimiter`.
        Only sets this property when the new parameter is after the current one.


        Args:
            new_last_invoked (datetime.datetime): new timestamp to set to, typically time of API call.
        """
        if new_last_invoked > self._last_invoked:
            for rate_limiter in self.rate_limiters:
                rate_limiter.last_invoked = new_last_invoked

    def reset(self) -> None:
        """
        Resets the `last_invoked` property of all member `RateLimiter`.
        """
        for rate_limiter in self.rate_limiters:
            rate_limiter.reset()

    def get_wait_time(self):
        """
        Calculates and returns whether user should wait before next call based on this limiter.
        Takes the max of all member `RateLimiter.get_wait_time()`!

        Returns:
            Optional[float]: None, if shouldn't wait. time-to-wait in seconds, if should wait.
        """
        durations = [rl.maybe_get_wait_duration() for rl in self.rate_limiters]
        durations = [d for d in durations if d is not None]
        return None if not durations else max(durations)


# V --------------- Riot API rate limiters --------------- V
DevelopmentKeyRateLimiters = RateLimiterCollection(
    rate_limiters=(
        RateLimiter(n_requests=20, per_interval="1seconds"),
        RateLimiter(n_requests=100, per_interval="2minutes"),
    )
)

PersonalKeyRateLimiters = RateLimiterCollection(
    rate_limiters=(
        RateLimiter(n_requests=20, per_interval="1seconds"),
        RateLimiter(n_requests=100, per_interval="2minutes"),
    )
)

ProductionKeyRateLimiters = RateLimiterCollection(
    rate_limiters=(
        RateLimiter(n_requests=500, per_interval="10seconds"),
        RateLimiter(n_requests=30_000, per_interval="10minutes"),
    )
)