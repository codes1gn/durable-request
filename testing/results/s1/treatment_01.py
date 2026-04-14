"""In-place reversal of a singly linked list."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def reverse_linked_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """Reverse the list in place; return the new head."""
    prev: Optional[ListNode] = None
    curr = head
    while curr is not None:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev
