"""Longest common prefix across a list of strings."""


def longest_common_prefix(strings: list[str]) -> str:
    """
    Return the longest prefix shared by every string in `strings`.
    If `strings` is empty, return ''.
    """
    if not strings:
        return ""
    reference = strings[0]
    for end in range(len(reference) + 1):
        prefix = reference[:end]
        for s in strings[1:]:
            if not s.startswith(prefix):
                return reference[: end - 1]
    return reference
