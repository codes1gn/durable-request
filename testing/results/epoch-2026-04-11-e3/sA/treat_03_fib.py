"""Memoized Fibonacci via functools.lru_cache."""

from functools import lru_cache


@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


if __name__ == "__main__":
    for i in range(15):
        print(f"fib({i}) = {fib(i)}")
