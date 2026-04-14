"""In-memory key-value store with optional per-entry TTL expiration."""

from __future__ import annotations

import time
from typing import Generic, Iterator, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class TTLKeyValueStore(Generic[K, V]):
    """
    Store arbitrary keys mapped to values. Each entry may expire after a TTL.

    Expiration uses ``time.monotonic()`` deadlines so behaviour is not affected
    by system clock adjustments. Expired entries are removed lazily on access.
    """

    __slots__ = ("_entries",)

    def __init__(self) -> None:
        # key -> (value, deadline_monotonic or None if no TTL)
        self._entries: dict[K, tuple[V, float | None]] = {}

    def set(self, key: K, value: V, ttl_seconds: float | None = None) -> None:
        """
        Associate ``value`` with ``key``.

        If ``ttl_seconds`` is None, the entry does not expire. Otherwise it is
        removed after ``ttl_seconds`` wall-clock seconds from this call.
        """
        deadline: float | None = None
        if ttl_seconds is not None:
            if ttl_seconds < 0:
                raise ValueError("ttl_seconds must be non-negative")
            deadline = time.monotonic() + ttl_seconds
        self._entries[key] = (value, deadline)

    def _is_expired(self, deadline: float | None) -> bool:
        if deadline is None:
            return False
        return time.monotonic() >= deadline

    def get(self, key: K, default: V | None = None) -> V | None:
        """
        Return the value for ``key``, or ``default`` if missing or expired.

        Like ``dict.get``, if ``default`` is None you cannot tell apart a stored
        ``None`` from a missing key without using ``key in store``.
        """
        item = self._entries.get(key)
        if item is None:
            return default
        value, deadline = item
        if self._is_expired(deadline):
            del self._entries[key]
            return default
        return value

    def delete(self, key: K) -> bool:
        """
        Remove ``key`` if present.

        Returns True if a (non-expired or expired) mapping was removed.
        """
        if key not in self._entries:
            return False
        del self._entries[key]
        return True

    def __contains__(self, key: object) -> bool:
        if key not in self._entries:
            return False
        _, deadline = self._entries[key]  # type: ignore[arg-type]
        if self._is_expired(deadline):
            del self._entries[key]  # type: ignore[arg-type]
            return False
        return True

    def __len__(self) -> int:
        self.cleanup_expired()
        return len(self._entries)

    def __iter__(self) -> Iterator[K]:
        self.cleanup_expired()
        return iter(self._entries)

    def keys(self) -> Iterator[K]:
        """Yield non-expired keys."""
        self.cleanup_expired()
        yield from self._entries

    def cleanup_expired(self) -> int:
        """
        Remove all expired entries.

        Returns the number of entries removed.
        """
        now = time.monotonic()
        expired = [k for k, (_, d) in self._entries.items() if d is not None and now >= d]
        for k in expired:
            del self._entries[k]
        return len(expired)
