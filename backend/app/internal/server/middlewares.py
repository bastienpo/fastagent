"""Collection of middlewares."""

import logging

from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class MaxSizeMiddleware(BaseHTTPMiddleware):
    """Limit the maximum size of the request body."""

    def __init__(self, app: ASGIApp, *, max_size: int | None = None) -> None:
        """Initialize the middleware.

        Args:
            app: The ASGI app.
            max_size: The maximum size of the request body.
        """
        super().__init__(app)
        self.max_size = max_size

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Call the middleware.

        This implementation comes from Litserve implementation.

        Args:
            scope: The scope.
            receive: The receive function.
            send: The send function.
        """
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        total_size = 0

        async def rcv() -> Message:
            """Receive a message."""
            nonlocal total_size
            message = await receive()

            chunk_size = len(message.get("body", b""))
            total_size += chunk_size

            if self.max_size is not None and total_size > self.max_size:
                raise HTTPException(413, "Payload too large")

            return message

        await self.app(scope, rcv, send)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Request logging middleware."""

    logger: logging.Logger

    def __init__(self, app: ASGIApp, logger: logging.Logger) -> None:
        """Initialize the middleware.

        Args:
            app: The ASGI app.
            logger: The logger.
        """
        super().__init__(app)
        self.logger = logger

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Dispatch the request.

        Args:
            request: The request.
            call_next: The next middleware or handler.

        Returns:
            The response.
        """
        self.logger.info("received request", extra={"request": request})
        return await call_next(request)
