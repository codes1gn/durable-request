"""Token bucket rate limiter."""

from __future__ import annotations

import threading
import time
from typing import Optional


class TokenBucket:
    """
    Token bucket rate limiter.

    Tokens refill continuously at ``rate`` tokens per second up to ``capacity``.
    """

    def __init__(self, capacity: float, rate: float) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if rate <= 0:
            raise ValueError("rate must be positive")
        self._capacity = float(capacity)
        self._rate = float(rate)
        self._tokens = self._capacity
        self._last = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self, now: float) -> None:
        elapsed = now - self._last
        self._last = now
        self._tokens = min(self._capacity, self._tokens + elapsed * self._rate)

    def consume(self, tokens: float = 1.0, *, block: bool = True, timeout: Optional[float] = None) -> bool:
        """
        Try to consume ``tokens`` from the bucket.

        If ``block`` is True, waits until tokens are available or ``timeout`` seconds elapse.
        Returns True if consumption succeeded, False otherwise.
        """
        if tokens <= 0:
            raise ValueError("tokens to consume must be positive")
        deadline = None if timeout is None else time.monotonic() + timeout
        while True:
            with self._lock:
                now = time.monotonic()
                self._refill(now)
                if self._tokens >= tokens:
                    self._tokens -= tokens
                    return True
                if not block:
                    return False
                if deadline is not None and now >= deadline:
                    return False
                # Time until one more token might appear (worst case wait for deficit)
                deficit = tokens - self._tokens
                wait = deficit / self._rate if self._rate > 0 else 0.0
                if deadline is not None:
                    wait = min(wait, max(0.0, deadline - now))
            time.sleep(min(wait, 0.05))

    @property
    def available(self) -> float:
        """Approximate tokens currently available (refreshed on read)."""
        with self._lock:
            self._refill(time.monotonic())
            return self._tokens
