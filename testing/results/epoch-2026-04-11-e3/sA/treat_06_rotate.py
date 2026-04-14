"""Rotate a list left by k positions (k may exceed list length)."""


def rotate_left(items: list, k: int) -> list:
    if not items:
        return []
    n = len(items)
    k = k % n
    return items[k:] + items[:k]


if __name__ == "__main__":
    xs = [1, 2, 3, 4, 5]
    for k in (0, 1, 2, 7):
        print(f"rotate_left({xs}, {k}) = {rotate_left(xs, k)}")
