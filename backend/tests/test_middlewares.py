"""Middlewares tests."""

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from app.internal.server.middlewares import MaxSizeMiddleware
from app.routers import agents


@pytest.fixture(scope="module")
def client() -> TestClient:
    """Setup the middleware."""
    app = FastAPI()
    app.include_router(agents.router)
    app.add_middleware(MaxSizeMiddleware, max_size=10)
    return TestClient(app)


def test_maxsize_middleware(client: TestClient) -> None:
    """Test the maxsize middleware."""
    payload = {"inputs": [{"topic": "Hello, world!"}]}

    response = client.post("/v1/agents/batch", json=payload)
    assert response.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
