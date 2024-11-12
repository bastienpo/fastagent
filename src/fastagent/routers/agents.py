"""Agent router."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from langserve import APIHandler
from sse_starlette import EventSourceResponse

from fastagent.internal.services import AgentBuilder

router = APIRouter(prefix="/v1", tags=["agent"])


async def _get_api_handler() -> APIHandler:
    """Setup an api handler for the chain."""
    builder = AgentBuilder().build()

    return APIHandler(builder, path="/agents")


APIHandlerDependency = Annotated[APIHandler, Depends(_get_api_handler)]


@router.post("/agents/invoke")
async def invoke_agents_handler(
    request: Request, runnable: APIHandlerDependency
) -> Response:
    """Handle invoke request."""
    return await runnable.invoke(request)


@router.post("/agents/batch")
async def batch_agents_handler(
    request: Request, runnable: APIHandlerDependency
) -> Response:
    """Handle batch request."""
    return await runnable.batch(request)


@router.post("/agents/stream")
async def stream_agents_handler(
    request: Request, runnable: APIHandlerDependency
) -> EventSourceResponse:
    """Handle stream request."""
    return await runnable.stream(request)
