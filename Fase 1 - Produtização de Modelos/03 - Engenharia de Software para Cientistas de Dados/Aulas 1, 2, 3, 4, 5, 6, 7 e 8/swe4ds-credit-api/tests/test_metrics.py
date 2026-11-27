"""Testes para o endpoint de métricas."""

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_metrics_endpoint_returns_counter():
    """Testa se o endpoint /metrics retorna contador de requisições."""
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "request_count" in data
    assert "status" in data
    assert isinstance(data["request_count"], int)


def test_metrics_endpoint_structure():
    """Testa a estrutura da resposta do endpoint /metrics."""
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["request_count"] >= 0
