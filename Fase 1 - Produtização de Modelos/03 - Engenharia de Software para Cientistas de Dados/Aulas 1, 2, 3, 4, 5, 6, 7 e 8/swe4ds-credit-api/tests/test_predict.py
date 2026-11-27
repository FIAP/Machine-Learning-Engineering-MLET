"""Testes para o endpoint de predição."""

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_predict_endpoint_with_valid_data():
    """Testa predição com dados válidos."""
    payload = {
        "age": 30,
        "income": 5000.0,
        "loan_amount": 10000.0,
        "credit_history": "good"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "confidence" in data
    assert data["prediction"] in ["approved", "rejected"]
    assert 0 <= data["confidence"] <= 1


def test_predict_endpoint_approved_scenario():
    """Testa cenário de aprovação."""
    payload = {
        "age": 35,
        "income": 8000.0,
        "loan_amount": 2000.0,
        "credit_history": "good"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == "approved"


def test_predict_endpoint_rejected_scenario():
    """Testa cenário de rejeição."""
    payload = {
        "age": 20,
        "income": 1000.0,
        "loan_amount": 50000.0,
        "credit_history": "poor"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == "rejected"


def test_predict_endpoint_with_invalid_age():
    """Testa predição com idade inválida."""
    payload = {
        "age": 15,  # Menor que 18
        "income": 5000.0,
        "loan_amount": 10000.0,
        "credit_history": "good"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # Validation error


def test_predict_endpoint_with_invalid_credit_history():
    """Testa predição com histórico de crédito inválido."""
    payload = {
        "age": 30,
        "income": 5000.0,
        "loan_amount": 10000.0,
        "credit_history": "invalid"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # Validation error


def test_predict_endpoint_with_missing_field():
    """Testa predição com campo obrigatório faltando."""
    payload = {
        "age": 30,
        "income": 5000.0,
        # loan_amount está faltando
        "credit_history": "good"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # Validation error
