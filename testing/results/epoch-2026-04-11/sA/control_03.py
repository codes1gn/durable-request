from __future__ import annotations

import functools
import time
from typing import Any, Callable, Tuple, Type, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def retry_with_exponential_backoff(
    *,
    max_attempts: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    multiplier: float = 2.0,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
) -> Callable[[F], F]:
    """
    Decorator factory: retry the wrapped callable on selected exceptions.

    After each failure, sleeps ``min(base_delay * multiplier**attempt, max_delay)``
    seconds before the next attempt. The first retry uses ``attempt == 0``.
    """

    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")
    if base_delay < 0 or max_delay < 0:
        raise ValueError("delays must be non-negative")
    if max_delay < base_delay:
        raise ValueError("max_delay must be >= base_delay")
    if multiplier < 1:
        raise ValueError("multiplier must be >= 1")

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == max_attempts - 1:
                        raise
                    delay = min(base_delay * (multiplier**attempt), max_delay)
                    time.sleep(delay)

        return wrapper  # type: ignore[return-value]

    return decorator
