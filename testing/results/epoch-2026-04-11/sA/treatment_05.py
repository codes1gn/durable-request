"""Token-bucket rate limiter for smooth bursty traffic shaping."""

from __future__ import annotations

import threading
import time


class TokenBucketRateLimiter:
    """
    Limits work to an average *rate* (tokens per second) while allowing bursts up to *capacity*.

    Tokens refill continuously based on elapsed time. The bucket holds at most *capacity*
    tokens. A caller spends tokens to proceed; if insufficient tokens remain, the caller
    may block or poll depending on the method used.
    """

    __slots__ = ("_capacity", "_rate", "_tokens", "_last_refill", "_lock")

    def __init__(self, rate: float, capacity: float | None = None) -> None:
        if rate <= 0:
            raise ValueError("rate must be positive")
        cap = capacity if capacity is not None else rate
        if cap <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = float(cap)
        self._rate = float(rate)
        self._tokens = self._capacity
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def _refill_locked(self, now: float) -> None:
        elapsed = now - self._last_refill
        if elapsed > 0:
            self._tokens = min(self._capacity, self._tokens + elapsed * self._rate)
            self._last_refill = now

    def available_tokens(self) -> float:
        """Approximate tokens currently in the bucket (refills based on monotonic clock)."""
        with self._lock:
            self._refill_locked(time.monotonic())
            return self._tokens

    def try_acquire(self, tokens: float = 1.0) -> bool:
        """
        Spend *tokens* if the bucket has enough after refill.

        Returns True if acquired, False without blocking otherwise.
        """
        if tokens <= 0:
            raise ValueError("tokens must be positive")
        with self._lock:
            now = time.monotonic()
            self._refill_locked(now)
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False

    def acquire(self, tokens: float = 1.0) -> None:
        """Block until *tokens* can be spent (may sleep)."""
        if tokens <= 0:
            raise ValueError("tokens must be positive")
        while True:
            wait: float
            with self._lock:
                now = time.monotonic()
                self._refill_locked(now)
                if self._tokens >= tokens:
                    self._tokens -= tokens
                    return
                deficit = tokens - self._tokens
                wait = deficit / self._rate if self._rate > 0 else 0.0
            time.sleep(min(wait, 0.25))

    def time_until_tokens(self, tokens: float = 1.0) -> float:
        """
        Seconds until *tokens* could be acquired without blocking (0 if available now).

        This does not consume tokens or mutate state beyond a refill for the readout.
        """
        if tokens <= 0:
            raise ValueError("tokens must be positive")
        with self._lock:
            now = time.monotonic()
            self._refill_locked(now)
            if self._tokens >= tokens:
                return 0.0
            deficit = tokens - self._tokens
            return deficit / self._rate
