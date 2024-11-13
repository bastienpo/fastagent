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
    server: Granian

    def _prepare_api(self, agent_module: AgentModule) -> None:
        """Prepare the API."""
        self._api.include_router(create_langchain_router(agent_module))
        self._api.include_router(healthcheck.router)

    def __init__(self, configuration: Configuration, agent_module: AgentModule) -> None:
        """Initialize the server."""
        self._prepare_api(agent_module)
        self._api.title = configuration.name

        target = "fastagent.internal.server.server:FastAgentServer._api"

        self.server = Granian(
            target=target,
            address="127.0.0.1",
            port=8000,
            reload=True,
            ssl_cert=None,
            ssl_key=None,
            interface="asgi",
            loop="uvloop",
            log_enabled=True,
        )

    def serve(self) -> None:
        """Serve the application."""
        self.server.serve()
