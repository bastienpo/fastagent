"""Main application file."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.internal.data.database import init_database
from app.internal.server.handlers import http_exception_handler
from app.internal.server.middlewares import (
    AuthenticationMiddleware,
    MaxSizeMiddleware,
    RequestLoggingMiddleware,
)
from app.internal.settings import Settings
from app.routers import agents, healthcheck, tokens, users

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage the lifespan of the application.

    Args:
        app: The FastAPI application.
    """
    dsn = Settings().database.get_dsn()
    app.async_pool = await init_database(dsn)
    logger.info("Connection to database opened")

    yield

    await app.async_pool.close()
    logger.info("Connection to database closed")


api = FastAPI(
    title="fastagent",
    version="0.0.1",
    lifespan=lifespan,
)
api.add_exception_handler(StarletteHTTPException, http_exception_handler)

api.include_router(healthcheck.router)
api.include_router(users.router)
api.include_router(tokens.router)
api.include_router(agents.router)


api.add_middleware(RequestLoggingMiddleware, logger=logger)
api.add_middleware(MaxSizeMiddleware, max_size=1024 * 1024)  # Approximatly 1 MB
api.add_middleware(CORSMiddleware, allow_origins=["*"])
api.add_middleware(AuthenticationMiddleware)
