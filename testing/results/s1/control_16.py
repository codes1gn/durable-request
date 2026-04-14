"""Context manager for database transaction handling."""

from __future__ import annotations

from contextlib import AbstractContextManager
from typing import Any, Callable, Optional, Protocol, TypeVar


class _Connection(Protocol):
    def commit(self) -> None: ...
    def rollback(self) -> None: ...


T_conn = TypeVar("T_conn", bound=_Connection)


class transaction(AbstractContextManager[T_conn]):
    """
    Context manager: ``commit()`` on clean exit, ``rollback()`` on exception.

    Usage::

        with transaction(conn) as c:
            c.execute(...)
    """

    def __init__(self, connection: T_conn) -> None:
        self._conn = connection

    def __enter__(self) -> T_conn:
        return self._conn

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[Any],
    ) -> None:
        if exc_type is None:
            self._conn.commit()
        else:
            self._conn.rollback()


def run_in_transaction(
    connection: T_conn,
    work: Callable[[T_conn], Any],
) -> Any:
    """Run ``work(conn)`` inside a transaction (commit/rollback)."""
    with transaction(connection) as conn:
        return work(conn)
