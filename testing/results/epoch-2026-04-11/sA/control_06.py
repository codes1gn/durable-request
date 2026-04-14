from __future__ import annotations

import logging
from typing import Any, Callable, List, Optional, TypeVar

T = TypeVar("T")


def merge_sort(
    items: List[T],
    *,
    key: Optional[Callable[[T], Any]] = None,
    logger: Optional[logging.Logger] = None,
    _depth: int = 0,
) -> List[T]:
    """
    Return a new list containing the elements of ``items`` in sorted order
    using merge sort. Every split, base case, comparison, pick, tail copy,
    and merge completion is logged at INFO when ``logger`` is provided.
    """
    log = logger or logging.getLogger(__name__)
    indent = "  " * _depth
    n = len(items)

    log.info("%sSTEP enter merge_sort depth=%d len=%d items=%r", indent, _depth, n, items)

    if n <= 1:
        log.info(
            "%sSTEP base case: len<=1, returning as-is -> %r",
            indent,
            list(items),
        )
        return list(items)

    mid = n // 2
    left = items[:mid]
    right = items[mid:]
    log.info(
        "%sSTEP split at mid=%d -> left(len=%d)=%r right(len=%d)=%r",
        indent,
        mid,
        len(left),
        left,
        len(right),
        right,
    )

    log.info("%sSTEP recurse left subtree", indent)
    sorted_left = merge_sort(left, key=key, logger=logger, _depth=_depth + 1)
    log.info("%sSTEP left subtree returned -> %r", indent, sorted_left)

    log.info("%sSTEP recurse right subtree", indent)
    sorted_right = merge_sort(right, key=key, logger=logger, _depth=_depth + 1)
    log.info("%sSTEP right subtree returned -> %r", indent, sorted_right)

    merged = _merge(
        sorted_left,
        sorted_right,
        key=key,
        log=log,
        indent=indent,
        depth=_depth,
    )
    log.info("%sSTEP merge complete depth=%d -> %r", indent, _depth, merged)
    return merged


def _merge(
    left: List[T],
    right: List[T],
    *,
    key: Optional[Callable[[T], Any]],
    log: logging.Logger,
    indent: str,
    depth: int,
) -> List[T]:
    """Merge two sorted sequences with per-comparison and per-pick logging."""

    def k(x: T) -> Any:
        return key(x) if key is not None else x

    out: List[T] = []
    i, j = 0, 0
    li, lj = len(left), len(right)

    log.info(
        "%sSTEP merge start depth=%d | left=%r | right=%r",
        indent,
        depth,
        left,
        right,
    )

    step_no = 0
    while i < li and j < lj:
        step_no += 1
        a, b = left[i], right[j]
        ka, kb = k(a), k(b)
        log.info(
            "%sSTEP merge[%d] compare left[%d]=%r (key=%r) vs right[%d]=%r (key=%r)",
            indent,
            step_no,
            i,
            a,
            ka,
            j,
            b,
            kb,
        )
        if ka <= kb:
            out.append(a)
            log.info(
                "%sSTEP merge[%d] pick LEFT -> out=%r",
                indent,
                step_no,
                out,
            )
            i += 1
        else:
            out.append(b)
            log.info(
                "%sSTEP merge[%d] pick RIGHT -> out=%r",
                indent,
                step_no,
                out,
            )
            j += 1

    if i < li:
        tail = left[i:]
        log.info(
            "%sSTEP merge flush remainder of LEFT from index %d: %r",
            indent,
            i,
            tail,
        )
        out.extend(tail)
    if j < lj:
        tail = right[j:]
        log.info(
            "%sSTEP merge flush remainder of RIGHT from index %d: %r",
            indent,
            j,
            tail,
        )
        out.extend(tail)

    log.info("%sSTEP merge finished depth=%d -> %r", indent, depth, out)
    return out


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    demo = [38, 27, 43, 3, 9, 82, 10]
    print("input:", demo)
    print("sorted:", merge_sort(demo, logger=logging.getLogger("mergesort.demo")))
