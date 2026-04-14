"""In-place reversal of a singly linked list."""


class ListNode:
    __slots__ = ("val", "next")

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverse_linked_list(head: ListNode | None) -> ListNode | None:
    """Reverse the list in place; return the new head."""
    prev = None
    cur = head
    while cur is not None:
        nxt = cur.next
        cur.next = prev
        prev = cur
        cur = nxt
    return prev
