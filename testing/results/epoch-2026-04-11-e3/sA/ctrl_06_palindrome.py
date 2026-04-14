"""Integer palindrome check."""


def is_palindrome(n: int) -> bool:
    """Return True if ``n`` reads the same forwards and backwards in base 10."""
    if n < 0:
        return False
    s = str(n)
    return s == s[::-1]
