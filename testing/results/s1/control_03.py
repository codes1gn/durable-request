"""LRU cache with O(1) average get and put via doubly linked list + hash map."""

from __future__ import annotations

from collections.abc import Hashable
from typing import Generic, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class _Node(Generic[K, V]):
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value
        self.prev: _Node[K, V] | None = None
        self.next: _Node[K, V] | None = None


class LRUCache(Generic[K, V]):
    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self._cap = capacity
        self._map: dict[K, _Node[K, V]] = {}
        self._head = _Node(None, None)  # type: ignore[arg-type]
        self._tail = _Node(None, None)  # type: ignore[arg-type]
        self._head.next = self._tail
        self._tail.prev = self._head

    def _unlink(self, node: _Node[K, V]) -> None:
        assert node.prev is not None and node.next is not None
        node.prev.next = node.next
        node.next.prev = node.prev

    def _to_front(self, node: _Node[K, V]) -> None:
        assert self._head.next is not None
        node.next = self._head.next
        node.prev = self._head
        self._head.next.prev = node
        self._head.next = node

    def get(self, key: K) -> V | None:
        if key not in self._map:
            return None
        node = self._map[key]
        self._unlink(node)
        self._to_front(node)
        return node.value

    def put(self, key: K, value: V) -> None:
        if key in self._map:
            node = self._map[key]
            node.value = value
            self._unlink(node)
            self._to_front(node)
            return
        if len(self._map) >= self._cap:
            assert self._tail.prev is not None and self._tail.prev is not self._head
            lru = self._tail.prev
            self._unlink(lru)
            del self._map[lru.key]
        node = _Node(key, value)
        self._map[key] = node
        self._to_front(node)
