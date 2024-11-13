"""The FastAgent server."""

from fastapi import FastAPI
from granian.server import Granian
from langchain_core.runnables import Runnable as LangchainRunnable

from fastagent.configuration import Configuration
from fastagent.integrations import create_langchain_router
from fastagent.routers import healthcheck

AgentModule = LangchainRunnable


class FastAgentServer:
    """The FastAgent server."""

    _api: FastAPI = FastAPI()
    _server: Granian
    _configuration: Configuration
    _agent_module: AgentModule

    def __init__(
        self: "FastAgentServer", configuration: Configuration, agent_module: AgentModule
    ) -> None:
        """Initialize the server.

        Args:
            configuration: The configuration.
            agent_module: The agent module.
        """
        self._api.title = configuration.project.name
        self._configuration = configuration
        self._agent_module = agent_module
        self._setup_api()

        _target = "fastagent.internal.server.server:FastAgentServer._api"

        self._server = Granian(
            target=_target,
            address="127.0.0.1",
            port=8000,
            reload=True,
            ssl_cert=None,
            ssl_key=None,
            interface="asgi",
            loop="uvloop",
            log_enabled=True,
        )

    def _setup_api(self: "FastAgentServer") -> None:
        """Setup required routes for the API.

        Args:
            agent_module: The agent module.
        """
        self._api.include_router(healthcheck.router)
        self._api.include_router(create_langchain_router(self._agent_module))

    def _setup_middlewares(self: "FastAgentServer") -> None:
        """Setup middlewares for the API."""

    def _setup_exception_handlers(self: "FastAgentServer") -> None:
        """Setup exception handlers for the API."""

    def _configure_lifespan(self: "FastAgentServer") -> None:
        """Configure the lifespan for the API."""

    def serve(self: "FastAgentServer") -> None:
        """Serve the application."""
        self._server.serve()
