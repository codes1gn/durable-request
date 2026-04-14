"""
Token bucket rate limiter.

Allows bursts up to `capacity` tokens; tokens refill continuously at `refill_rate`
tokens per second.
"""

from __future__ import annotations

import time
from typing import Optional


class TokenBucketRateLimiter:
    """
    Thread-safe enough for single-threaded use; for multi-threaded scenarios
    protect `try_consume` with a lock.
    """

    def __init__(self, capacity: float, refill_rate: float) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if refill_rate <= 0:
            raise ValueError("refill_rate must be positive")
        self._capacity = float(capacity)
        self._refill_rate = float(refill_rate)
        self._tokens = float(capacity)
        self._last_refill = time.monotonic()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._last_refill = now
        self._tokens = min(self._capacity, self._tokens + elapsed * self._refill_rate)

    @property
    def tokens_available(self) -> float:
        self._refill()
        return self._tokens

    def try_consume(self, tokens: float = 1.0) -> bool:
        """Return True if `tokens` were deducted, False if not enough capacity."""
        if tokens <= 0:
            raise ValueError("tokens must be positive")
        self._refill()
        if self._tokens >= tokens:
            self._tokens -= tokens
            return True
        return False

    def consume(self, tokens: float = 1.0, block: bool = False, timeout: Optional[float] = None) -> bool:
        """
        Consume tokens, optionally blocking until available or timeout.

        When block=False, behaves like try_consume.
        When block=True, sleeps until tokens are available or timeout elapses.
        """
        if not block:
            return self.try_consume(tokens)
        deadline = None if timeout is None else (time.monotonic() + timeout)
        while True:
            if self.try_consume(tokens):
                return True
            if deadline is not None and time.monotonic() >= deadline:
                return False
            # Need rate; estimate wait for one token worth of refill
            need = tokens - self.tokens_available
            wait = max(0.0, need / self._refill_rate)
            if deadline is not None:
                wait = min(wait, max(0.0, deadline - time.monotonic()))
            time.sleep(min(wait, 0.05))
