"""Binary search on a sorted sequence."""


def binary_search(sorted_seq: list[int], target: int) -> int | None:
    """
    Return the index of `target` in `sorted_seq`, or None if not present.
    `sorted_seq` must be sorted in ascending order.
    """
    lo, hi = 0, len(sorted_seq) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        v = sorted_seq[mid]
        if v == target:
            return mid
        if v < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return None
