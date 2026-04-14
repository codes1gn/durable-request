"""Simple in-memory key-value store with TTL expiration."""

from __future__ import annotations

import threading
import time
from typing import Any, Dict, Iterator, Optional, Tuple


class TTLStore:
    """Key-value store where each entry can expire after a time-to-live (seconds)."""

    def __init__(self) -> None:
        self._data: Dict[str, Tuple[Any, Optional[float]]] = {}
        self._lock = threading.RLock()

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """Set ``key`` to ``value``. If ``ttl`` is None, the key does not expire."""
        if ttl is not None and ttl < 0:
            raise ValueError("ttl must be non-negative or None")
        deadline = None if ttl is None else time.monotonic() + ttl
        with self._lock:
            self._data[key] = (value, deadline)

    def get(self, key: str, default: Any = None) -> Any:
        """Return value for ``key`` if present and not expired, else ``default``."""
        with self._lock:
            if key not in self._data:
                return default
            value, deadline = self._data[key]
            if deadline is not None and time.monotonic() >= deadline:
                del self._data[key]
                return default
            return value

    def delete(self, key: str) -> bool:
        """Remove ``key``. Returns True if it existed."""
        with self._lock:
            if key in self._data:
                del self._data[key]
                return True
            return False

    def __contains__(self, key: str) -> bool:
        with self._lock:
            if key not in self._data:
                return False
            _value, deadline = self._data[key]
            if deadline is not None and time.monotonic() >= deadline:
                del self._data[key]
                return False
            return True

    def __len__(self) -> int:
        self.cleanup_expired()
        with self._lock:
            return len(self._data)

    def keys(self) -> Iterator[str]:
        self.cleanup_expired()
        with self._lock:
            yield from list(self._data.keys())

    def cleanup_expired(self) -> int:
        """Remove all expired keys. Returns number of keys removed."""
        now = time.monotonic()
        removed = 0
        with self._lock:
            dead = [k for k, (_, d) in self._data.items() if d is not None and now >= d]
            for k in dead:
                del self._data[k]
                removed += 1
        return removed
