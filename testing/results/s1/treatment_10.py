"""Prime number generator using the Sieve of Eratosthenes (incremental / unbounded)."""

from __future__ import annotations

from collections import defaultdict
from typing import Iterator


def primes_sieve() -> Iterator[int]:
    """
    Yield primes in increasing order using an incremental Sieve of Eratosthenes.

    This is the unbounded variant: each composite is crossed off by its least
    prime factor, matching the classical sieve rule without fixing an upper bound.
    """
    # Maps composite -> list of primes that divide it (for wheel of cancellations)
    composite_to_primes: dict[int, list[int]] = defaultdict(list)
    candidate = 2
    while True:
        if candidate not in composite_to_primes:
            yield candidate
            composite_to_primes[candidate * candidate].append(candidate)
        else:
            for p in composite_to_primes[candidate]:
                composite_to_primes[p + candidate].append(p)
            del composite_to_primes[candidate]
        candidate += 1
