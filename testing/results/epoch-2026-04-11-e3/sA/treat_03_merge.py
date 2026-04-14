"""Merge two sorted lists into one sorted list in O(n + m) time."""


def merge_sorted(a: list[int], b: list[int]) -> list[int]:
    i, j = 0, 0
    out: list[int] = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out


if __name__ == "__main__":
    print(merge_sorted([1, 3, 5], [2, 4, 6]))
