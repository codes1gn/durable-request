"""LRU cache with O(1) average get and put (hash map + doubly linked list)."""

from __future__ import annotations

from typing import Any, Optional


class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: int, value: Any) -> None:
        self.key = key
        self.value = value
        self.prev: Optional[_Node] = None
        self.next: Optional[_Node] = None


class LRUCache:
    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self._cap = capacity
        self._map: dict[int, _Node] = {}
        self._head = _Node(0, None)  # sentinel head
        self._tail = _Node(0, None)  # sentinel tail
        self._head.next = self._tail
        self._tail.prev = self._head

    def _unlink(self, node: _Node) -> None:
        assert node.prev is not None and node.next is not None
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node: _Node) -> None:
        nxt = self._head.next
        assert nxt is not None
        node.prev = self._head
        node.next = nxt
        self._head.next = node
        nxt.prev = node

    def get(self, key: int) -> Any:
        if key not in self._map:
            return None
        node = self._map[key]
        self._unlink(node)
        self._add_front(node)
        return node.value

    def put(self, key: int, value: Any) -> None:
        if key in self._map:
            node = self._map[key]
            node.value = value
            self._unlink(node)
            self._add_front(node)
            return
        if len(self._map) >= self._cap:
            lru = self._tail.prev
            assert lru is not None and lru is not self._head
            self._unlink(lru)
            del self._map[lru.key]
        node = _Node(key, value)
        self._map[key] = node
        self._add_front(node)
