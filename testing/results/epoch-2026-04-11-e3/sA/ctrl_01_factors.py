from __future__ import annotations


def prime_factors(n: int) -> list[int]:
    """Return all prime factors of n with multiplicity, in non-decreasing order."""
    if n < 2:
        return []
    factors: list[int] = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        factors.append(n)
    return factors
