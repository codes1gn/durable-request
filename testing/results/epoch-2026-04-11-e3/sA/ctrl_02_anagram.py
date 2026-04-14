"""Check whether two strings are anagrams of each other."""


def are_anagrams(a: str, b: str) -> bool:
    """
    Return True if `a` and `b` are anagrams (same multiset of characters).
    Comparison is case-sensitive; whitespace counts.
    """
    if len(a) != len(b):
        return False
    counts: dict[str, int] = {}
    for ch in a:
        counts[ch] = counts.get(ch, 0) + 1
    for ch in b:
        if ch not in counts:
            return False
        counts[ch] -= 1
        if counts[ch] < 0:
            return False
    return all(v == 0 for v in counts.values())
