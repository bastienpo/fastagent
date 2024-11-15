"""The FastAgent server."""

import logging
from typing import Literal

from fastapi import FastAPI
from granian.server import Granian
from starlette.exceptions import HTTPException as StarletteHTTPException

from fastagent.configuration import Config
from fastagent.dependencies import require_auth_dependency
from fastagent.integrations import create_langchain_router
from fastagent.internal import ModuleLoader
from fastagent.internal.data.database import init_database
from fastagent.internal.log import setup_logger
from fastagent.internal.server import (
    AuthenticationMiddleware,
    RequestLoggingMiddleware,
    http_exception_handler,
)
from fastagent.routers import healthcheck, tokens, users


class FastAgentServer:
    """The FastAgent server ."""

    _api: FastAPI = FastAPI()
    _server: Granian
    _logger: logging.Logger = setup_logger(level=logging.INFO)
    configuration: Config
    environment: Literal["dev", "prod"]

    def __init__(
        self: "FastAgentServer",
        configuration: Config,
        environment: Literal["dev", "prod"],
    ) -> None:
        """Initialize the server from the configuration and agent module.

        Args:
            configuration: The configuration.
            environment: The environment of the application.
        """
        self.configuration = configuration
        self.environment = environment

        # Setups
        self.setup_api()
        self.setup_middlewares()

        # setup exception handlers
        self._api.add_exception_handler(StarletteHTTPException, http_exception_handler)

        self._api.add_event_handler("startup", self.startup_lifespan())
        self._api.add_event_handler("shutdown", self.shutdown_lifespan())

        # Target is the ASGI application created in the same file.
        # This is a workaround to make granian work with FastAPI.
        # This could lead to issues in the future.
        target = "fastagent.server:FastAgentServer._api"

        self._server = Granian(
            target=target,
            address=self.configuration.server.host,
            port=self.configuration.server.port,
            reload=self.environment == "dev",
            interface="asgi",
            loop="uvloop",
            log_enabled=False,
            log_level=self.configuration.server.log_level,
        )

    def setup_api(self: "FastAgentServer") -> None:
        """Setup required routes for the API.

        Args:
            agent_module: The agent module.
        """
        # Default routers
        self._api.include_router(healthcheck.router)
        target_module = ModuleLoader.load_from_string(self.configuration.project.app)

        # Business logic routers
        match self.configuration.project.framework:
            case "langchain":
                if self.configuration.security.authentication:
                    self._api.include_router(
                        create_langchain_router(target_module),
                        dependencies=[require_auth_dependency],
                    )
                else:
                    self._api.include_router(create_langchain_router(target_module))
            case _:
                message = (
                    f"Unsupported framework: {self.configuration.project.framework}"
                    f"fastagent only supports langchain at the moment. Expecting more soon."  # noqa: E501
                )
                raise ValueError(message)

        if self.configuration.security.authentication:
            self._api.include_router(users.router)
            self._api.include_router(tokens.router)

    def setup_middlewares(self: "FastAgentServer") -> None:
        """Setup middlewares for the API.

        Setup the middleware according to the configuration.
        """
        # Default middlewares
        self._api.add_middleware(RequestLoggingMiddleware, logger=self._logger)

        # Add an authentication middleware if authentication is enabled
        if self.configuration.security.authentication:
            self._api.add_middleware(AuthenticationMiddleware)

    def startup_lifespan(self: "FastAgentServer") -> None:
        """Startup the lifespan of the application."""
        test_dsn = (
            "postgresql://postgres:postgres@localhost:5432/fastagent?sslmode=disable"
        )

        async def startup() -> None:
            """Startup the application."""
            self._logger.info("Starting application")

            if self.configuration.storage.database == "postgresql":
                self._api.async_pool = await init_database(test_dsn)
                self._logger.info("Connection to database established")

        return startup

    def shutdown_lifespan(self: "FastAgentServer") -> None:
        """Shutdown the lifespan of the application."""

        async def shutdown() -> None:
            """Shutdown the application."""
            if self.configuration.storage.database == "postgresql":
                await self._api.async_pool.close()
                self._logger.info("Connection to database closed")

            self._logger.info("Shutting down server")

        return shutdown

    def serve(self: "FastAgentServer") -> None:
        """Serve the application."""
        self._server.serve()
