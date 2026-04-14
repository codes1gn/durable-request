"""Flatten a nested list of arbitrary depth."""


def flatten(nested) -> list:
    """
    Return a new list containing all non-list elements from `nested`,
    in depth-first order. Empty lists are skipped.
    """
    out: list = []
    stack = [nested]
    while stack:
        item = stack.pop()
        if isinstance(item, list):
            for child in reversed(item):
                stack.append(child)
        else:
            out.append(item)
    return out
