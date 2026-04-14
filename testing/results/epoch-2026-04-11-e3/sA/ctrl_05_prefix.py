def longest_common_prefix(strings: list[str]) -> str:
    """Return the longest prefix shared by all strings in `strings`. Empty list -> ''."""
    if not strings:
        return ""
    first = strings[0]
    for i, ch in enumerate(first):
        for s in strings[1:]:
            if i >= len(s) or s[i] != ch:
                return first[:i]
    return first
