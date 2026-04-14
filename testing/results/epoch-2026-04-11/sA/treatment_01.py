"""In-place reversal of a singly linked list."""


class ListNode:
    """Node in a singly linked list."""

    __slots__ = ("val", "next")

    def __init__(self, val: object, next_: "ListNode | None" = None) -> None:
        self.val = val
        self.next = next_


def reverse_linked_list(head: ListNode | None) -> ListNode | None:
    """
    Reverse the list starting at head in O(n) time and O(1) extra space.

    Returns the new head (former tail), or None if head was None.
    """
    prev: ListNode | None = None
    current = head
    while current is not None:
        nxt = current.next
        current.next = prev
        prev = current
        current = nxt
    return prev
