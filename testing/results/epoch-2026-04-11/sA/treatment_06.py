"""Merge sort with detailed step-by-step logging."""

from __future__ import annotations

import logging
from collections.abc import Callable, MutableSequence
from typing import TypeVar

T = TypeVar("T")


def merge_sort(
    items: MutableSequence[T],
    *,
    key: Callable[[T], object] | None = None,
    logger: logging.Logger | None = None,
) -> None:
    """
    Sort ``items`` in ascending order using merge sort (stable).

    Logs each divide, recursive boundary, merge comparison, and copy so the
    algorithm can be traced from the logs alone. Uses ``logger`` if provided;
    otherwise the ``merge_sort`` named logger at INFO level (no handler by
    default—call ``logging.basicConfig`` or attach a handler to see output).
    """
    log = logger or logging.getLogger("merge_sort")
    if not log.handlers and logger is None:
        # Reasonable default for scripts: one-line INFO to stderr.
        _h = logging.StreamHandler()
        _h.setFormatter(logging.Formatter("%(message)s"))
        log.addHandler(_h)
        log.setLevel(logging.INFO)
        log.propagate = False  # avoid duplicate lines if root also has handlers

    n = len(items)
    if n <= 1:
        log.info("merge_sort: length=%s — nothing to sort, returning", n)
        return

    aux: list[T] = list(items)

    def merge_sort_range(lo: int, hi: int, depth: int) -> None:
        indent = "  " * depth
        span = hi - lo + 1
        log.info(
            "%sdivide: range [%s, %s] (size=%s) slice=%r",
            indent,
            lo,
            hi,
            span,
            list(items[lo : hi + 1]),
        )
        if lo >= hi:
            log.info("%sbase case: single element at index %s — no merge", indent, lo)
            return

        mid = (lo + hi) // 2
        log.info("%ssplit at mid=%s → left [%s,%s] right [%s,%s]", indent, mid, lo, mid, mid + 1, hi)

        log.info("%srecurse LEFT on [%s, %s]", indent, lo, mid)
        merge_sort_range(lo, mid, depth + 1)
        log.info("%srecurse RIGHT on [%s, %s]", indent, mid + 1, hi)
        merge_sort_range(mid + 1, hi, depth + 1)

        log.info(
            "%smerge: combining sorted left %r with right %r",
            indent,
            list(items[lo : mid + 1]),
            list(items[mid + 1 : hi + 1]),
        )

        i, j, k = lo, mid + 1, lo
        cmp_count = 0
        while i <= mid and j <= hi:
            cmp_count += 1
            left_key = key(items[i]) if key else items[i]
            right_key = key(items[j]) if key else items[j]
            log.info(
                "%s  compare #%s: left[%s]=%r vs right[%s]=%r",
                indent,
                cmp_count,
                i,
                items[i],
                j,
                items[j],
            )
            if left_key <= right_key:
                log.info("%s  take from LEFT → aux[%s] = %r", indent, k, items[i])
                aux[k] = items[i]
                i += 1
            else:
                log.info("%s  take from RIGHT → aux[%s] = %r", indent, k, items[j])
                aux[k] = items[j]
                j += 1
            k += 1

        while i <= mid:
            log.info("%s  drain LEFT: aux[%s] = %r", indent, k, items[i])
            aux[k] = items[i]
            i += 1
            k += 1
        while j <= hi:
            log.info("%s  drain RIGHT: aux[%s] = %r", indent, k, items[j])
            aux[k] = items[j]
            j += 1
            k += 1

        for t in range(lo, hi + 1):
            items[t] = aux[t]
        log.info("%smerged range [%s, %s] is now: %r", indent, lo, hi, list(items[lo : hi + 1]))

    log.info("merge_sort: start length=%s initial=%r", n, list(items))
    merge_sort_range(0, n - 1, 0)
    log.info("merge_sort: done final=%r", list(items))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    demo = [38, 27, 43, 3, 9, 82, 10]
    merge_sort(demo)
    print("sorted:", demo)
