"""Prime number generator using a segmented Sieve of Eratosthenes."""

from __future__ import annotations

import math
from collections.abc import Iterator


def _eratosthenes_upto(n: int) -> list[int]:
    """All primes <= n (classic sieve)."""
    if n < 2:
        return []
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(math.isqrt(n)) + 1):
        if sieve[p]:
            sieve[p * p : n + 1 : p] = b"\x00" * (((n - p * p) // p) + 1)
    return [i for i in range(2, n + 1) if sieve[i]]


def primes() -> Iterator[int]:
    """
    Yield primes in increasing order using segmented Eratosthenes sieving.

    Each window [low, hi) is sieved using all primes <= isqrt(hi - 1) from a
    small upfront sieve, which is the standard segmented sieve recipe.
    """
    yield 2
    low = 3
    span = 300_000
    while True:
        hi = low + span
        lim = int(math.isqrt(hi - 1)) + 1
        small_primes = _eratosthenes_upto(lim)
        size = hi - low
        is_comp = bytearray(size)
        for p in small_primes:
            p2 = p * p
            start = p2 if p2 >= low else ((low + p - 1) // p) * p
            if start < low:
                start += p
            for m in range(start, hi, p):
                is_comp[m - low] = 1
        for i in range(size):
            v = low + i
            if v >= 2 and not is_comp[i]:
                yield v
        low = hi
