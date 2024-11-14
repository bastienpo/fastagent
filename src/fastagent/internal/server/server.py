"""The FastAgent server."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from granian.server import Granian
from starlette.exceptions import HTTPException as StarletteHTTPException

from fastagent.configuration import Config
from fastagent.dependencies import require_auth_dependency
from fastagent.integrations import create_langchain_router
from fastagent.internal import ModuleLoader
from fastagent.internal.data.database import init_database
from fastagent.internal.server import (
    AuthenticationMiddleware,
    RequestLoggingMiddleware,
    http_exception_handler,
)
from fastagent.routers import healthcheck, tokens, users

logger = logging.getLogger(__name__)


class FastAgentServer:
    """The FastAgent server ."""

    _api: FastAPI = FastAPI()
    _server: Granian
    _configuration: Config

    def __init__(self: "FastAgentServer", configuration: Config) -> None:
        """Initialize the server from the configuration and agent module.

        Args:
            configuration: The configuration.
        """
        self._configuration = configuration

        # Setups
        self._setup_api()
        self._setup_middlewares()
        self._setup_exception_handlers()
        self._api.add_event_handler("startup", self.startup_lifespan())
        self._api.add_event_handler("shutdown", self.shutdown_lifespan())

        # Target is the ASGI application created in the same file.
        # This is a workaround to make granian work with FastAPI.
        # This could lead to issues in the future.
        _target = "fastagent.internal.server.server:FastAgentServer._api"

        self._server = Granian(
            target=_target,
            address=self._configuration.server.host,
            port=self._configuration.server.port,
            reload=self._configuration.server._reload,
            ssl_cert=None,
            ssl_key=None,
            interface="asgi",
            loop="uvloop",
            log_enabled=self._configuration.server._logging,
        )

    def _setup_api(self: "FastAgentServer") -> None:
        """Setup required routes for the API.

        Args:
            agent_module: The agent module.
        """
        # Default routers
        self._api.include_router(healthcheck.router)
        target_module = ModuleLoader.load_from_string(self._configuration.project.app)

        # Business logic routers
        match self._configuration.project.framework:
            case "langchain":
                if self._configuration.security.authentication:
                    self._api.include_router(
                        create_langchain_router(target_module),
                        dependencies=[require_auth_dependency],
                    )
                else:
                    self._api.include_router(create_langchain_router(target_module))
            case _:
                message = (
                    f"Unsupported framework: {self._configuration.project.framework}"
                    f"fastagent only supports langchain at the moment. Expecting more soon."  # noqa: E501
                )
                raise ValueError(message)

        if self._configuration.security.authentication:
            self._api.include_router(users.router)
            self._api.include_router(tokens.router)

    def _setup_middlewares(self: "FastAgentServer") -> None:
        """Setup middlewares for the API.

        Setup the middleware according to the configuration.
        """
        # Default middlewares
        self._api.add_middleware(RequestLoggingMiddleware, logger=logger)

        # Add an authentication middleware if authentication is enabled
        if self._configuration.security.authentication:
            self._api.add_middleware(AuthenticationMiddleware)

    def _setup_exception_handlers(self: "FastAgentServer") -> None:
        """Setup exception handlers for the API."""
        self._api.add_exception_handler(StarletteHTTPException, http_exception_handler)

    def startup_lifespan(self: "FastAgentServer") -> None:
        """Startup the lifespan of the application."""
        test_dsn = (
            "postgresql://postgres:postgres@localhost:5432/fastagent?sslmode=disable"
        )

        async def startup() -> None:
            """Startup the application."""
            if self._configuration.project.database == "postgresql":
                self._api.async_pool = await init_database(test_dsn)
                logger.info("Connection to database opened")

        return startup

    def shutdown_lifespan(self: "FastAgentServer") -> None:
        """Shutdown the lifespan of the application."""

        async def shutdown() -> None:
            """Shutdown the application."""
            if self._configuration.project.database == "postgresql":
                await self._api.async_pool.close()
                logger.info("Connection to database closed")

        return shutdown

    def serve(self: "FastAgentServer") -> None:
        """Serve the application."""
        self._server.serve()
