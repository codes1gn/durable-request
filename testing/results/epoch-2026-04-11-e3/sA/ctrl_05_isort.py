def insertion_sort(items: list) -> list:
    """Sort `items` in ascending order using insertion sort (in-place). Returns the same list."""
    for i in range(1, len(items)):
        key = items[i]
        j = i - 1
        while j >= 0 and items[j] > key:
            items[j + 1] = items[j]
            j -= 1
        items[j + 1] = key
    return items
