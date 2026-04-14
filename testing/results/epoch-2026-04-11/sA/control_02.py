"""O(1) LRU cache: hash map + doubly linked list (frequency order)."""


class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: int, value: int) -> None:
        self.key = key
        self.value = value
        self.prev: _Node | None = None
        self.next: _Node | None = None


class LRUCache:
    """
    Least-recently-used eviction cache with O(1) average-case get and put.

    Doubly linked list holds (key, value) nodes in usage order (MRU near tail,
    LRU near head). A dict maps each key to its node for O(1) lookup.
    """

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._cap = capacity
        self._map: dict[int, _Node] = {}
        self._head = _Node(0, 0)
        self._tail = _Node(0, 0)
        self._head.next = self._tail
        self._tail.prev = self._head

    def _remove(self, node: _Node) -> None:
        assert node.prev is not None and node.next is not None
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_tail(self, node: _Node) -> None:
        assert self._tail.prev is not None
        p = self._tail.prev
        p.next = node
        node.prev = p
        node.next = self._tail
        self._tail.prev = node

    def get(self, key: int) -> int:
        """Return value for key, or -1 if missing."""
        node = self._map.get(key)
        if node is None:
            return -1
        self._remove(node)
        self._add_to_tail(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        """Insert or update key; evict LRU if at capacity."""
        if key in self._map:
            node = self._map[key]
            node.value = value
            self._remove(node)
            self._add_to_tail(node)
            return

        if len(self._map) >= self._cap:
            assert self._head.next is not None
            lru = self._head.next
            self._remove(lru)
            del self._map[lru.key]

        node = _Node(key, value)
        self._map[key] = node
        self._add_to_tail(node)
