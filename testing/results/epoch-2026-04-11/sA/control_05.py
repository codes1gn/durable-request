from __future__ import annotations

import threading
import time
from typing import Optional


class TokenBucketRateLimiter:
    """
    Token bucket rate limiter.

    Tokens refill continuously at ``rate`` per second up to ``capacity``.
    Each granted request debits tokens from the bucket; bursts are allowed
    up to ``capacity`` when the bucket is full.
    """

    __slots__ = ("_capacity", "_rate", "_tokens", "_last_refill", "_lock")

    def __init__(self, rate: float, capacity: float) -> None:
        if rate <= 0:
            raise ValueError("rate must be positive")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = float(capacity)
        self._rate = float(rate)
        self._tokens = self._capacity
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    @property
    def capacity(self) -> float:
        return self._capacity

    @property
    def rate(self) -> float:
        return self._rate

    def _refill(self, now: float) -> None:
        elapsed = now - self._last_refill
        if elapsed > 0:
            self._tokens = min(self._capacity, self._tokens + elapsed * self._rate)
            self._last_refill = now

    def available_tokens(self) -> float:
        """Approximate tokens currently in the bucket (refills first)."""
        with self._lock:
            self._refill(time.monotonic())
            return self._tokens

    def try_consume(self, tokens: float = 1.0) -> bool:
        """
        Attempt to take ``tokens`` from the bucket without blocking.

        Returns True if the debit succeeded, False if insufficient tokens.
        """
        if tokens <= 0:
            raise ValueError("tokens must be positive")
        with self._lock:
            now = time.monotonic()
            self._refill(now)
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False

    def consume(
        self,
        tokens: float = 1.0,
        *,
        timeout: Optional[float] = None,
    ) -> bool:
        """
        Block until ``tokens`` can be debited or ``timeout`` seconds elapse.

        Returns True if tokens were consumed, False on timeout (non-blocking
        if ``timeout`` is 0.0). If ``timeout`` is None, waits indefinitely.
        """
        if tokens <= 0:
            raise ValueError("tokens must be positive")
        deadline: Optional[float] = None
        if timeout is not None:
            if timeout < 0:
                raise ValueError("timeout must be non-negative")
            deadline = time.monotonic() + timeout

        while True:
            with self._lock:
                now = time.monotonic()
                self._refill(now)
                if self._tokens >= tokens:
                    self._tokens -= tokens
                    return True
                if deadline is not None and now >= deadline:
                    return False
                shortfall = tokens - self._tokens
                wait = shortfall / self._rate if self._rate > 0 else 0.0
                if deadline is not None:
                    wait = min(wait, max(0.0, deadline - now))

            if wait > 0:
                time.sleep(wait)
            else:
                # Avoid busy spin when rounding leaves a tiny positive wait.
                time.sleep(0)
