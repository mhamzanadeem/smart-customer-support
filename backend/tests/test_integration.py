from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "database" in data


def test_keepalive():
    response = client.get("/api/keepalive")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "smart-customer-support"
    assert "timestamp" in data


def test_debug_ping():
    response = client.get("/api/debug/ping")
    assert response.status_code == 200
    assert response.json()["message"] == "backend reachable"


def test_chat_invalid_input():
    response = client.post(
        "/api/chat",
        json={"query": ""},
    )
    assert response.status_code == 422


def test_chat_missing_query():
    response = client.post(
        "/api/chat",
        json={},
    )
    assert response.status_code == 422
