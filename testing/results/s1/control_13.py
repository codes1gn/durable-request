"""Merge sort with detailed step logging."""

from __future__ import annotations

from typing import Any, Callable, List, TypeVar

T = TypeVar("T")


def merge_sort_logged(
    arr: List[T],
    log: Callable[[str], None] | None = None,
    key: Callable[[T], Any] | None = None,
) -> List[T]:
    """
    Return a new sorted list using merge sort.

    Calls ``log`` with human-readable messages for each recursive step and merge.
    """
    if log is None:
        log = lambda _msg: None  # noqa: E731

    def sort_slice(items: List[T], label: str) -> List[T]:
        n = len(items)
        log(f"enter {label}: len={n} items={items!r}")
        if n <= 1:
            log(f"base case {label}: return {items!r}")
            return list(items)
        mid = n // 2
        left = items[:mid]
        right = items[mid:]
        log(f"split {label} -> left={left!r}, right={right!r}")
        sorted_left = sort_slice(left, f"{label}.L")
        sorted_right = sort_slice(right, f"{label}.R")
        merged = _merge(sorted_left, sorted_right, key, log, f"{label}.merge")
        log(f"exit {label}: merged={merged!r}")
        return merged

    return sort_slice(list(arr), "root")


def _merge(
    left: List[T],
    right: List[T],
    key: Callable[[T], Any] | None,
    log: Callable[[str], None],
    label: str,
) -> List[T]:
    log(f"{label}: merging left={left!r} right={right!r}")
    i = j = 0
    out: List[T] = []
    kf = (lambda x: x) if key is None else key
    while i < len(left) and j < len(right):
        if kf(left[i]) <= kf(right[j]):
            log(f"{label}: take left[{i}]={left[i]!r}")
            out.append(left[i])
            i += 1
        else:
            log(f"{label}: take right[{j}]={right[j]!r}")
            out.append(right[j])
            j += 1
    while i < len(left):
        log(f"{label}: flush left[{i}]={left[i]!r}")
        out.append(left[i])
        i += 1
    while j < len(right):
        log(f"{label}: flush right[{j}]={right[j]!r}")
        out.append(right[j])
        j += 1
    log(f"{label}: result={out!r}")
    return out
