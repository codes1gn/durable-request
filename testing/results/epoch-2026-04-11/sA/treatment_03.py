"""Decorator: retry a callable on selected exceptions with exponential backoff."""

from __future__ import annotations

import functools
import random
import time
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def retry_on_exception(
    *,
    max_attempts: int = 5,
    base_delay: float = 0.5,
    max_delay: float = 30.0,
    backoff: float = 2.0,
    jitter: float = 0.1,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Return a decorator that retries the wrapped function with exponential backoff.

    After each failure, sleep for ``min(max_delay, base_delay * backoff**attempt)``
    plus optional uniform jitter in ``[0, jitter]`` seconds (when ``jitter > 0``).

    On the final attempt, failures propagate without another sleep.
    """

    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")
    if base_delay < 0 or max_delay < 0:
        raise ValueError("delays must be non-negative")
    if backoff < 1:
        raise ValueError("backoff must be >= 1")
    if jitter < 0:
        raise ValueError("jitter must be non-negative")

    def decorator(fn: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exc: BaseException | None = None
            for attempt in range(max_attempts):
                try:
                    return fn(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    if attempt == max_attempts - 1:
                        raise
                    delay = min(max_delay, base_delay * (backoff**attempt))
                    if jitter > 0:
                        delay += random.uniform(0.0, jitter)
                    time.sleep(delay)
            assert last_exc is not None
            raise last_exc

        return wrapper

    return decorator


# Example (not executed on import):
if __name__ == "__main__":

    @retry_on_exception(max_attempts=4, base_delay=0.1, exceptions=(ValueError,))
    def flaky(x: int) -> int:
        if x < 3:
            raise ValueError("not yet")
        return x

    print(flaky(3))
