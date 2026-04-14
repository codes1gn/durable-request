"""Greatest common divisor via the Euclidean algorithm."""


def gcd(a: int, b: int) -> int:
    """Return the greatest common divisor of ``a`` and ``b`` (non-negative)."""
    x, y = abs(a), abs(b)
    while y:
        x, y = y, x % y
    return x
