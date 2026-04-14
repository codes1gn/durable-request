"""Merge two sorted lists into one sorted list."""


def merge_sorted(a: list, b: list) -> list:
    """Return a new sorted list containing all elements from sorted iterables a and b."""
    i, j = 0, 0
    out: list = []
    la, lb = len(a), len(b)
    while i < la and j < lb:
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    if i < la:
        out.extend(a[i:])
    if j < lb:
        out.extend(b[j:])
    return out
