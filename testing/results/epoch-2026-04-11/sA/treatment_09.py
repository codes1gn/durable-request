"""Binary search tree with insert, delete, and search."""


from __future__ import annotations


class _Node:
    __slots__ = ("key", "left", "right")

    def __init__(self, key: int) -> None:
        self.key = key
        self.left: _Node | None = None
        self.right: _Node | None = None


class BinarySearchTree:
    """Integer-key BST; duplicate keys are ignored on insert."""

    def __init__(self) -> None:
        self._root: _Node | None = None

    @property
    def root(self) -> _Node | None:
        return self._root

    def search(self, key: int) -> bool:
        """Return True if key is in the tree."""
        return self._search_node(self._root, key) is not None

    def insert(self, key: int) -> None:
        """Insert key if not already present."""
        self._root = self._insert(self._root, key)

    def delete(self, key: int) -> None:
        """Remove key if present; no-op if absent."""
        self._root = self._delete(self._root, key)

    def _search_node(self, node: _Node | None, key: int) -> _Node | None:
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search_node(node.left, key)
        return self._search_node(node.right, key)

    def _insert(self, node: _Node | None, key: int) -> _Node:
        if node is None:
            return _Node(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        return node

    def _min_node(self, node: _Node) -> _Node:
        while node.left is not None:
            node = node.left
        return node

    def _delete(self, node: _Node | None, key: int) -> _Node | None:
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            succ = self._min_node(node.right)
            node.key = succ.key
            node.right = self._delete(node.right, succ.key)
        return node
