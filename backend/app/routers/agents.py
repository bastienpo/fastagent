"""Agent router."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from langserve import APIHandler
from sse_starlette import EventSourceResponse

from app.internal.agent import chain

router = APIRouter(prefix="/v1", tags=["agent"])


async def _get_api_handler() -> APIHandler:
    """Prepare a RunnableLambda."""
    return APIHandler(chain, path="/agents")


@router.post("/agents/invoke")
async def invoke_agents_handler(
    request: Request, runnable: Annotated[APIHandler, Depends(_get_api_handler)]
) -> Response:
    """Handle invoke request."""
    return await runnable.invoke(request)


@router.post("/agents/stream")
async def stream_agents_handler(
    request: Request, runnable: Annotated[APIHandler, Depends(_get_api_handler)]
) -> EventSourceResponse:
    """Handle stream request."""
    return await runnable.stream(request)
