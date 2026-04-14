"""
Context manager for database transaction handling (DB-API style).
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Generator, Optional, Protocol


class _Connection(Protocol):
    def commit(self) -> None: ...
    def rollback(self) -> None: ...


@contextmanager
def transaction(conn: _Connection) -> Generator[None, None, None]:
    """
    On normal exit: commit. On exception: rollback, then re-raise.

    Expects ``conn`` to provide ``commit()`` and ``rollback()`` like PEP 249 connections.
    """
    try:
        yield
    except BaseException:
        conn.rollback()
        raise
    else:
        conn.commit()


class DatabaseTransaction:
    """
    Class-based context manager with optional savepoint-style nesting
    (each instance commits/rollbacks the same connection on exit).
    """

    def __init__(self, conn: _Connection) -> None:
        self._conn = conn
        self._finished = False

    def __enter__(self) -> "DatabaseTransaction":
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc: Optional[BaseException],
        tb: Any,
    ) -> None:
        if self._finished:
            return None
        self._finished = True
        if exc_type is not None:
            self._conn.rollback()
            return None
        self._conn.commit()
        return None
