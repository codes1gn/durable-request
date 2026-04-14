"""Retry decorator with exponential backoff on exceptions."""

from __future__ import annotations

import functools
import random
import time
from collections.abc import Callable
from typing import Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def retry_on_exception(
    *,
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float | None = None,
    exponential_base: float = 2.0,
    jitter: bool = True,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
) -> Callable[[F], F]:
    """
    Retry the wrapped function when it raises one of `exceptions`.

    Delay before attempt k (k >= 2) is min(max_delay, base_delay * exponential_base ** (k-2)),
    optionally multiplied by a random factor in [0.5, 1.5] if jitter is True.
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exc: BaseException | None = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    if attempt == max_attempts:
                        raise
                    exp = base_delay * (exponential_base ** (attempt - 1))
                    if max_delay is not None:
                        exp = min(exp, max_delay)
                    if jitter:
                        exp *= 0.5 + random.random()
                    time.sleep(exp)
            assert last_exc is not None
            raise last_exc

        return wrapper  # type: ignore[return-value]

    return decorator
