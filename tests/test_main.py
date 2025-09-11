"""Test Main Endpoints."""

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_home() -> None:
    """Test '/'."""
    response = client.get("/")
    assert response.status_code == 200  # noqa: PLR2004


def test_healthcheck() -> None:
    """Test '/healthcheck'."""
    response = client.get("/healthcheck")
    assert response.status_code == 200  # noqa: PLR2004
    assert response.text == "OK"
