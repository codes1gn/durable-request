"""Least-recently-used (LRU) cache with O(1) average get and put."""

from __future__ import annotations

from typing import Dict, Generic, Hashable, Optional, TypeVar, cast

KT = TypeVar("KT", bound=Hashable)
VT = TypeVar("VT")


class _Node(Generic[KT, VT]):
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: KT, value: VT) -> None:
        self.key = key
        self.value = value
        self.prev: Optional[_Node[KT, VT]] = None
        self.next: Optional[_Node[KT, VT]] = None


class LRUCache(Generic[KT, VT]):
    """Hash map plus doubly linked list for O(1) get and put."""

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = capacity
        self._map: Dict[KT, _Node[KT, VT]] = {}
        _ph = object()
        self._head = _Node(cast(KT, _ph), cast(VT, _ph))
        self._tail = _Node(cast(KT, _ph), cast(VT, _ph))
        self._head.prev = None
        self._head.next = self._tail
        self._tail.prev = self._head
        self._tail.next = None

    def get(self, key: KT) -> Optional[VT]:
        node = self._map.get(key)
        if node is None:
            return None
        self._move_to_front(node)
        return node.value

    def put(self, key: KT, value: VT) -> None:
        node = self._map.get(key)
        if node is not None:
            node.value = value
            self._move_to_front(node)
            return

        new_node = _Node(key, value)
        self._map[key] = new_node
        self._add_to_front(new_node)

        if len(self._map) > self._capacity:
            lru = self._tail.prev
            assert lru is not None and lru is not self._head
            self._remove(lru)
            del self._map[lru.key]

    def _add_to_front(self, node: _Node[KT, VT]) -> None:
        nxt = self._head.next
        assert nxt is not None
        node.prev = self._head
        node.next = nxt
        self._head.next = node
        nxt.prev = node

    def _remove(self, node: _Node[KT, VT]) -> None:
        assert node.prev is not None and node.next is not None
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_front(self, node: _Node[KT, VT]) -> None:
        self._remove(node)
        self._add_to_front(node)
