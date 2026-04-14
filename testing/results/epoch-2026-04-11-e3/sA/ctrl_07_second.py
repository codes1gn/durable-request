"""Second largest distinct value in a list."""


def second_largest(items: list) -> object:
    """
    Return the second largest distinct value in `items`.

    Raises ValueError if there are fewer than two distinct comparable values.
    Elements must be hashable (for ``set``).
    """
    unique = sorted(set(items))
    if len(unique) < 2:
        raise ValueError("list must contain at least two distinct values")
    return unique[-2]
