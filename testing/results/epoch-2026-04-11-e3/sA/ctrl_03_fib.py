"""Fibonacci with memoization."""

from functools import lru_cache


@lru_cache(maxsize=None)
def fibonacci(n: int) -> int:
    """Return the nth Fibonacci number (0-indexed: F(0)=0, F(1)=1)."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
