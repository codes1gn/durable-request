"""Simple ASGI middleware that logs each HTTP request and response status."""

from __future__ import annotations

import logging
import time
from collections.abc import Awaitable, Callable
from typing import Any

logger = logging.getLogger(__name__)

ASGIApp = Callable[
    [
        dict[str, Any],
        Callable[[], Awaitable[dict[str, Any]]],
        Callable[[dict[str, Any]], Awaitable[None]],
    ],
    Awaitable[None],
]


class RequestLoggingMiddleware:
    """
    ASGI middleware: logs method, path, client, elapsed time, and status code.

    Compatible with Starlette, FastAPI, and other ASGI servers.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(
        self,
        scope: dict[str, Any],
        receive: Callable[[], Awaitable[dict[str, Any]]],
        send: Callable[[dict[str, Any]], Awaitable[None]],
    ) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        method = scope.get("method", "?")
        path = scope.get("path", "?")
        client = scope.get("client")
        client_s = f"{client[0]}:{client[1]}" if client else "-"
        start = time.perf_counter()
        status_code: int | None = None

        async def send_wrapper(message: dict[str, Any]) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = int(message["status"])
            await send(message)

        await self.app(scope, receive, send_wrapper)
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        logger.info(
            "%s %s -> %s | %.2f ms | %s",
            method,
            path,
            status_code if status_code is not None else "?",
            elapsed_ms,
            client_s,
        )
