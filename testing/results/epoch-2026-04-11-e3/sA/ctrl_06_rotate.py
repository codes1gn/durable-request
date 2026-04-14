"""List rotation."""


def rotate_list(items: list, k: int) -> list:
    """Return a new list equal to ``items`` rotated **right** by ``k`` indices (cyclic).

    Empty lists are returned unchanged. ``k`` may be any integer; it is reduced modulo length.
    """
    if not items:
        return []
    n = len(items)
    k = k % n
    if k == 0:
        return list(items)
    return items[-k:] + items[:-k]
