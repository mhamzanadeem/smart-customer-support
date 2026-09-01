import pytest
from unittest.mock import patch, MagicMock

from src.services.database import (
    ping_database,
    check_mongodb_health,
)


@patch("src.services.database.get_client")
def test_ping_database_success(mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    assert ping_database() is True


@patch("src.services.database.get_client", side_effect=Exception("Connection failed"))
def test_ping_database_failure(mock_get_client):
    assert ping_database() is False


@patch("src.services.database.get_client")
def test_check_mongodb_health_connected(mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    result = check_mongodb_health()
    assert result["status"] == "connected"
    assert "latency_ms" in result


@patch("src.services.database.get_client", side_effect=Exception("timeout"))
def test_check_mongodb_health_error(mock_get_client):
    result = check_mongodb_health()
    assert result["status"] == "error"
