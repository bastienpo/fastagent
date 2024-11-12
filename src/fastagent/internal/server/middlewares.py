"""Collection of middlewares."""

import logging

from fastapi import HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from fastagent.internal.data.tokens import TOKEN_LENGTH
from fastagent.internal.data.tokens import Scope as TokenScope
from fastagent.internal.data.users import AnnonymousUser, get_user_for_token
from fastagent.internal.server.context import Context


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
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="Payload too large",
                )

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


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Authentication middleware."""

    def __init__(self, app: ASGIApp) -> None:
        """Initialize the middleware.

        Args:
            app: The ASGI app.
        """
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response | JSONResponse:
        """Dispatch the request."""
        authorization = request.headers.get("Authorization")

        if authorization is None or authorization == "":
            # If token is not provided, use anonymous user
            request.state.context = Context(user=AnnonymousUser)
        elif not authorization.startswith("Bearer "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Invalid token format, Token should start with 'Bearer '"
                },
                headers={"Vary": "Authorization"},
            )
        else:
            token = authorization.split(" ")[1]

            # Token format validation
            if len(token) != TOKEN_LENGTH:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Invalid token format"},
                    headers={"Vary": "Authorization"},
                )

            # Retrieve user from token
            async with request.app.async_pool.acquire() as conn:
                try:
                    user = await get_user_for_token(
                        conn, TokenScope.AUTHENTICATION, token
                    )
                except ValueError:
                    return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={"detail": "Invalid token"},
                        headers={"Vary": "Authorization"},
                    )

            request.state.context = Context(user=user)

        response = await call_next(request)
        response.headers["Vary"] = "Authorization"

        # Clean up context
        request.state.context = None

        return response
