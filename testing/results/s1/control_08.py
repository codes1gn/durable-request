"""Simple HTTP request logging middleware (ASGI)."""

from __future__ import annotations

import logging
import time
from collections.abc import Awaitable, Callable

logger = logging.getLogger(__name__)

ASGIApp = Callable[
    [Callable[..., Awaitable[None]], dict, Callable[..., Awaitable[None]]],
    Awaitable[None],
]


class RequestLoggerMiddleware:
    """
    ASGI middleware that logs method, path, status, and duration per request.
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(
        self,
        scope: dict,
        receive: Callable[..., Awaitable[None]],
        send: Callable[..., Awaitable[None]],
    ) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        method = scope.get("method", "?")
        path = scope.get("path", "")
        query = scope.get("query_string", b"").decode("latin-1")
        if query:
            path = f"{path}?{query}"

        start = time.perf_counter()
        status_holder: list[int | None] = [None]

        async def send_wrapper(message: dict) -> None:
            if message["type"] == "http.response.start":
                status_holder[0] = message["status"]
            await send(message)

        await self.app(scope, receive, send_wrapper)
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        status = status_holder[0] if status_holder[0] is not None else 0
        logger.info(
            "%s %s -> %s %.2fms",
            method,
            path,
            status,
            elapsed_ms,
        )
