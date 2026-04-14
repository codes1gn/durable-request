"""Binary search tree: insert, delete, search."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterator, Optional


@dataclass
class BSTNode:
    key: Any
    left: Optional["BSTNode"] = None
    right: Optional["BSTNode"] = None


class BinarySearchTree:
    def __init__(self) -> None:
        self._root: Optional[BSTNode] = None

    def search(self, key: Any) -> Optional[BSTNode]:
        return self._search(self._root, key)

    def _search(self, node: Optional[BSTNode], key: Any) -> Optional[BSTNode]:
        if node is None:
            return None
        if key == node.key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def insert(self, key: Any) -> None:
        self._root = self._insert(self._root, key)

    def _insert(self, node: Optional[BSTNode], key: Any) -> BSTNode:
        if node is None:
            return BSTNode(key=key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        return node

    def delete(self, key: Any) -> None:
        self._root = self._delete(self._root, key)

    def _delete(self, node: Optional[BSTNode], key: Any) -> Optional[BSTNode]:
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

    @staticmethod
    def _min_node(node: BSTNode) -> BSTNode:
        while node.left is not None:
            node = node.left
        return node

    def inorder(self) -> Iterator[Any]:
        yield from self._inorder(self._root)

    def _inorder(self, node: Optional[BSTNode]) -> Iterator[Any]:
        if node is None:
            return
        yield from self._inorder(node.left)
        yield node.key
        yield from self._inorder(node.right)
