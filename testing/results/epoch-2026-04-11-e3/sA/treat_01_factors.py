"""Prime factorization."""


def prime_factors(n: int) -> list[int]:
    """Return all prime factors of *n* (with multiplicity), sorted ascending.

    For n < 2, returns an empty list.
    """
    if n < 2:
        return []
    factors: list[int] = []
    x = n
    d = 2
    while d * d <= x:
        while x % d == 0:
            factors.append(d)
            x //= d
        d += 1 if d == 2 else 2
    if x > 1:
        factors.append(x)
    return factors
