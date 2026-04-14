"""Insertion sort for sequences."""


def insertion_sort(items: list) -> list:
    """
    Sort `items` in ascending order using insertion sort (in-place).
    Returns the same list object.
    """
    n = len(items)
    for i in range(1, n):
        value = items[i]
        j = i - 1
        while j >= 0 and items[j] > value:
            items[j + 1] = items[j]
            j -= 1
        items[j + 1] = value
    return items
