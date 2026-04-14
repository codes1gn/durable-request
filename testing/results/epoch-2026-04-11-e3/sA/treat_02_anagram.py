"""Anagram checking."""


def is_anagram(a: str, b: str) -> bool:
    """
    Return True if `a` and `b` are anagrams (same multiset of characters,
    case-sensitive). Whitespace and punctuation count as characters.
    """
    if len(a) != len(b):
        return False
    return sorted(a) == sorted(b)
