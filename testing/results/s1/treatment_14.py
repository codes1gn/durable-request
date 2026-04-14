"""
Simple in-memory key-value store with per-key TTL expiration.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Dict, Iterator, Optional, Tuple


@dataclass
class _Entry:
    value: Any
    expires_at: float


class TTLKVStore:
    """String keys; values are arbitrary objects. Expired keys behave as missing."""

    def __init__(self) -> None:
        self._data: Dict[str, _Entry] = {}

    def set(self, key: str, value: Any, ttl_seconds: float) -> None:
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        self._data[key] = _Entry(value=value, expires_at=time.monotonic() + ttl_seconds)

    def get(self, key: str) -> Optional[Any]:
        entry = self._data.get(key)
        if entry is None:
            return None
        if time.monotonic() >= entry.expires_at:
            del self._data[key]
            return None
        return entry.value

    def delete(self, key: str) -> bool:
        return self._data.pop(key, None) is not None

    def cleanup_expired(self) -> int:
        """Remove all expired keys. Returns count removed."""
        now = time.monotonic()
        dead = [k for k, e in self._data.items() if now >= e.expires_at]
        for k in dead:
            del self._data[k]
        return len(dead)

    def __len__(self) -> int:
        self.cleanup_expired()
        return len(self._data)

    def items(self) -> Iterator[Tuple[str, Any]]:
        self.cleanup_expired()
        for k, e in self._data.items():
            yield k, e.value
