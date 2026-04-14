"""
Merge sort with detailed step logging.
"""

from __future__ import annotations

from typing import Any, Callable, List, Optional, TypeVar

T = TypeVar("T")


def merge_sort_with_logging(
    items: List[T],
    *,
    key: Optional[Callable[[T], Any]] = None,
    log: Optional[Callable[[str], None]] = None,
) -> List[T]:
    """
    Return a new sorted list using merge sort. Logs merge and split steps via `log`.

    Args:
        items: Sequence to sort (copied; original unchanged).
        key: Optional key function like ``list.sort`` key=.
        log: If provided, called with human-readable step descriptions.
    """
    if log is None:
        log = lambda _m: None

    arr = list(items)
    n = len(arr)

    def compare(a: T, b: T) -> bool:
        ka = key(a) if key else a
        kb = key(b) if key else b
        return ka <= kb

    def merge(left: List[T], right: List[T], depth: int) -> List[T]:
        log(
            f"merge: depth={depth} merging left={left!r} right={right!r}"
        )
        i = j = 0
        out: List[T] = []
        while i < len(left) and j < len(right):
            if compare(left[i], right[j]):
                out.append(left[i])
                i += 1
            else:
                out.append(right[j])
                j += 1
        out.extend(left[i:])
        out.extend(right[j:])
        log(f"merge: depth={depth} result={out!r}")
        return out

    def sort_range(lo: int, hi: int, depth: int) -> List[T]:
        segment = arr[lo:hi]
        log(f"split: depth={depth} range=[{lo}:{hi}] segment={segment!r}")
        if hi - lo <= 1:
            log(f"base: depth={depth} leaf={segment!r}")
            return segment
        mid = (lo + hi) // 2
        left = sort_range(lo, mid, depth + 1)
        right = sort_range(mid, hi, depth + 1)
        return merge(left, right, depth)

    log(f"start: n={n} input={arr!r}")
    if n == 0:
        log("done: empty input")
        return []
    result = sort_range(0, n, 0)
    log(f"done: sorted={result!r}")
    return result
