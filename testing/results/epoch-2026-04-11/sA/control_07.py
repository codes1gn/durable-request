from __future__ import annotations

import time
from typing import Any, Dict, Iterator, Optional, Tuple


class TTLKeyValueStore:
    """
    In-memory string-keyed store with optional per-entry TTL (seconds).

    Expiration uses a monotonic clock so entries are not affected by system
    time adjustments. Expired entries are removed on read and omitted from
    iteration helpers.
    """

    __slots__ = ("_data",)

    def __init__(self) -> None:
        # key -> (value, expiry_monotonic or None if no TTL)
        self._data: Dict[str, Tuple[Any, Optional[float]]] = {}

    def set(self, key: str, value: Any, ttl_seconds: Optional[float] = None) -> None:
        """Associate key with value. If ttl_seconds is set, the entry expires after that many seconds."""
        if ttl_seconds is not None and ttl_seconds < 0:
            raise ValueError("ttl_seconds must be non-negative")
        deadline: Optional[float] = None
        if ttl_seconds is not None:
            deadline = time.monotonic() + float(ttl_seconds)
        self._data[key] = (value, deadline)

    def get(self, key: str, default: Any = None) -> Any:
        """Return the value for key, or default if missing or expired (expired entries are deleted)."""
        entry = self._data.get(key)
        if entry is None:
            return default
        value, deadline = entry
        if deadline is not None and time.monotonic() >= deadline:
            del self._data[key]
            return default
        return value

    def delete(self, key: str) -> bool:
        """Remove key. Returns True if a live entry was removed."""
        if key not in self._data:
            return False
        entry = self._data[key]
        _, deadline = entry
        if deadline is not None and time.monotonic() >= deadline:
            del self._data[key]
            return False
        del self._data[key]
        return True

    def __contains__(self, key: object) -> bool:
        if not isinstance(key, str):
            return False
        return self.get(key, default=_MISSING) is not _MISSING

    def __len__(self) -> int:
        self._purge_expired()
        return len(self._data)

    def keys(self) -> Iterator[str]:
        """Yield non-expired keys."""
        self._purge_expired()
        yield from self._data.keys()

    def items(self) -> Iterator[Tuple[str, Any]]:
        """Yield (key, value) pairs for non-expired entries."""
        self._purge_expired()
        for k, (v, _) in self._data.items():
            yield k, v

    def clear(self) -> None:
        self._data.clear()

    def _purge_expired(self) -> None:
        now = time.monotonic()
        dead = [
            k
            for k, (_, deadline) in self._data.items()
            if deadline is not None and now >= deadline
        ]
        for k in dead:
            del self._data[k]


class _Missing:
    pass


_MISSING = _Missing()
