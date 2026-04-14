"""Reverse each word's characters while preserving word order."""

import re


def reverse_words_in_sentence(sentence: str) -> str:
    """
    Reverse the characters inside each word; spaces and word order stay the same.

    Example: "hello world" -> "olleh dlrow"
    """
    if not sentence:
        return sentence

    def rev_word(match: re.Match[str]) -> str:
        return match.group(0)[::-1]

    return re.sub(r"\S+", rev_word, sentence)
