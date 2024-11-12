"""Tests for handlers."""

from fastapi import status
from fastapi.testclient import TestClient

from src.fastagent.dependencies import require_auth
from app.main import api

client = TestClient(app=api)
# Disable authentication for testing
api.dependency_overrides[require_auth] = lambda: None


def test_healthcheck() -> None:
    """Test the healthcheck handler."""
    response = client.get("/v1/healthcheck")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "available",
        "system_info": {"version": "0.0.1", "environment": "development"},
    }


def test_invoke_agent() -> None:
    """Test the invoke agent handler.

    JSON output is not deterministic, so we can't test the exact output.
    """
    payload = {"input": {"topic": "Hello, world!"}}

    response = client.post("/v1/agents/invoke", json=payload)
    assert response.status_code == status.HTTP_200_OK


def test_batch_invoke_agent() -> None:
    """Test the batch invoke agent handler."""
    payload = {"inputs": [{"topic": "Hello, world!"}]}

    response = client.post("/v1/agents/batch", json=payload)
    assert response.status_code == status.HTTP_200_OK
