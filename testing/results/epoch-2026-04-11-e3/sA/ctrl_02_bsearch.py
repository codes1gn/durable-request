"""Binary search on a sorted list of comparable elements."""


def binary_search(sorted_list: list, target) -> int:
    """
    Return the index of `target` in `sorted_list`, or -1 if not present.
    `sorted_list` must be sorted in ascending order.
    """
    lo, hi = 0, len(sorted_list) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        val = sorted_list[mid]
        if val == target:
            return mid
        if val < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
