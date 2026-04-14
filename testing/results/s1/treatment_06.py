"""Decorator that retries a callable on specified exceptions with exponential backoff."""

from __future__ import annotations

import functools
import logging
import random
import time
from typing import Any, Callable, ParamSpec, Tuple, Type, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

logger = logging.getLogger(__name__)


def retry_on_exception(
    *,
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
    on_retry: Callable[[BaseException, int], None] | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Retry the wrapped function when it raises one of ``exceptions``.

    Delay before attempt *k* (1-based after the first failure) is
    ``min(max_delay, base_delay * exponential_base ** (k - 1))``, optionally
    multiplied by a random factor in ``(0, 1]`` when ``jitter`` is True.
    """

    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")
    if base_delay < 0 or max_delay < 0:
        raise ValueError("delays must be non-negative")
    if exponential_base < 1:
        raise ValueError("exponential_base must be >= 1")

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exc: BaseException | None = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    if attempt >= max_attempts:
                        break
                    delay = min(max_delay, base_delay * (exponential_base ** (attempt - 1)))
                    if jitter:
                        delay *= random.random() or 1e-9
                    if on_retry is not None:
                        on_retry(e, attempt)
                    else:
                        logger.warning(
                            "%s failed (attempt %s/%s): %s; sleeping %.4fs",
                            func.__name__,
                            attempt,
                            max_attempts,
                            e,
                            delay,
                        )
                    time.sleep(delay)
            assert last_exc is not None
            raise last_exc

        return wrapper

    return decorator
