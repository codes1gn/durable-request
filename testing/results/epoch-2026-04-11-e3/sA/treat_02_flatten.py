"""Flatten arbitrarily nested lists."""


def flatten(nested: list) -> list:
    """
    Return a new list with all non-list elements from `nested` in depth-first
    order. List/tuple elements are recursed into; other iterables are not
    flattened (treated as atomic values).
    """
    out: list = []
    for item in nested:
        if isinstance(item, list):
            out.extend(flatten(item))
        else:
            out.append(item)
    return out
