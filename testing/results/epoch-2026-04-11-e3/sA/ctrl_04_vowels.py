"""Count vowels and consonants in a string (letters only; case-insensitive)."""

VOWELS = frozenset("aeiou")


def count_vowels_consonants(text: str) -> tuple[int, int]:
    """
    Return (vowel_count, consonant_count) for alphabetic characters in `text`.
    Non-letters are ignored.
    """
    vowels = 0
    consonants = 0
    for ch in text.lower():
        if not ch.isalpha():
            continue
        if ch in VOWELS:
            vowels += 1
        else:
            consonants += 1
    return vowels, consonants
