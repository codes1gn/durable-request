from __future__ import annotations

from typing import Optional


class ListNode:
    """Singly linked list node."""

    __slots__ = ("val", "next")

    def __init__(self, val: int = 0, next: Optional[ListNode] = None) -> None:
        self.val = val
        self.next = next


def reverse_linked_list_in_place(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Reverse a singly linked list in-place by rewiring .next pointers.

    Returns the new head (former tail). O(n) time, O(1) extra space.
    """
    prev: Optional[ListNode] = None
    curr = head
    while curr is not None:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev
