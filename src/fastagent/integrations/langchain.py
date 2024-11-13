"""Agent router."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from langchain_core.runnables import Runnable
from langserve import APIHandler
from sse_starlette import EventSourceResponse


def create_langchain_router(runnable: Runnable, prefix: str = "/v1") -> APIRouter:
    """Create a router for the agent."""
    router = APIRouter(prefix=prefix, tags=["agent"])

    async def _get_invoke_handler() -> APIHandler:
        return APIHandler(runnable, path="/agents")

    @router.post("/agents/invoke")
    async def invoke_agents_handler(
        request: Request, runnable: Annotated[APIHandler, Depends(_get_invoke_handler)]
    ) -> Response:
        """Handle invoke request."""
        return await runnable.invoke(request)

    @router.post("/agents/batch")
    async def batch_agents_handler(
        request: Request, runnable: Annotated[APIHandler, Depends(_get_invoke_handler)]
    ) -> Response:
        """Handle batch request."""
        return await runnable.batch(request)

    @router.post("/agents/stream")
    async def stream_agents_handler(
        request: Request, runnable: Annotated[APIHandler, Depends(_get_invoke_handler)]
    ) -> EventSourceResponse:
        """Handle stream request."""
        return await runnable.stream(request)

    return router
