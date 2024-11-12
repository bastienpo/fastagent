"""Common handlers."""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """Starlette HTTP exception handler.

    Args:
        request: The request.
        exc: The exception.

    Returns:
        The response as a JSON object.
    """
    match exc.status_code:
        case status.HTTP_404_NOT_FOUND:
            msg = "the requested resource was not found."
        case status.HTTP_405_METHOD_NOT_ALLOWED:
            msg = f"the method {request.method} is not supported for this resource."
        case _:
            msg = exc.detail

    return JSONResponse(status_code=exc.status_code, content={"message": msg})
