from __future__ import annotations

from typing import Optional


class BSTNode:
    """Node in a binary search tree keyed by integer values."""

    __slots__ = ("val", "left", "right")

    def __init__(
        self,
        val: int,
        left: Optional[BSTNode] = None,
        right: Optional[BSTNode] = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right


class BinarySearchTree:
    """
    Integer BST: left subtree values < node value; right subtree values > node value.
    Duplicate values are ignored on insert.
    """

    __slots__ = ("root",)

    def __init__(self) -> None:
        self.root: Optional[BSTNode] = None

    def search(self, key: int) -> bool:
        """Return True if key exists in the tree."""
        return self._search_node(self.root, key) is not None

    def _search_node(self, node: Optional[BSTNode], key: int) -> Optional[BSTNode]:
        if node is None:
            return None
        if key == node.val:
            return node
        if key < node.val:
            return self._search_node(node.left, key)
        return self._search_node(node.right, key)

    def insert(self, key: int) -> None:
        """Insert key if not already present."""
        self.root = self._insert_node(self.root, key)

    def _insert_node(self, node: Optional[BSTNode], key: int) -> BSTNode:
        if node is None:
            return BSTNode(key)
        if key < node.val:
            node.left = self._insert_node(node.left, key)
        elif key > node.val:
            node.right = self._insert_node(node.right, key)
        return node

    def delete(self, key: int) -> None:
        """Remove key if present; no-op if missing."""
        self.root = self._delete_node(self.root, key)

    def _delete_node(self, node: Optional[BSTNode], key: int) -> Optional[BSTNode]:
        if node is None:
            return None
        if key < node.val:
            node.left = self._delete_node(node.left, key)
        elif key > node.val:
            node.right = self._delete_node(node.right, key)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            succ = self._min_node(node.right)
            node.val = succ.val
            node.right = self._delete_node(node.right, succ.val)
        return node

    @staticmethod
    def _min_node(node: BSTNode) -> BSTNode:
        cur = node
        while cur.left is not None:
            cur = cur.left
        return cur
