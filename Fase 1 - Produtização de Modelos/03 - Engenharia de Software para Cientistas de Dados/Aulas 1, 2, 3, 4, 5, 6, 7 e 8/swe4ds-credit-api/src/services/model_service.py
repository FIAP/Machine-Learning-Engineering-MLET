"""Serviço de modelo de ML (simulado)."""

import json
import logging
from pathlib import Path

logger = logging.getLogger("credit-api")

# Caminho para logs de drift
DRIFT_LOG_PATH = Path("logs/input_samples.jsonl")


def load_model():
    """
    Carrega o modelo de ML.
    
    Nota: Por enquanto é um modelo simulado.
    Em produção, carregaria um modelo real treinado.
    
    Returns:
        dict: Configuração do modelo simulado
    """
    logger.info("Loading model...")
    return {
        "type": "simulated",
        "version": "0.1.0",
        "threshold": 0.6,
    }


def predict_one(data: dict) -> dict:
    """
    Realiza predição para um único registro.
    
    Args:
        data: Dicionário com features do cliente
        
    Returns:
        dict: Resultado da predição
    """
    # Lógica de predição simulada baseada em regras simples
    age = data.get("age", 0)
    income = data.get("income", 0)
    loan_amount = data.get("loan_amount", 0)
    credit_history = data.get("credit_history", "poor")
    
    # Score simulado
    score = 0.5
    
    # Ajustes baseados em features
    if credit_history == "good":
        score += 0.3
    elif credit_history == "fair":
        score += 0.1
    
    if age >= 25 and age <= 55:
        score += 0.1
    
    if income > loan_amount * 3:
        score += 0.2
    elif income > loan_amount * 2:
        score += 0.1
    
    # Limita entre 0 e 1
    score = min(1.0, max(0.0, score))
    
    # Decisão
    prediction = "approved" if score >= 0.6 else "rejected"
    
    return {
        "prediction": prediction,
        "confidence": round(score, 3),
    }


def log_input_sample(payload: dict) -> None:
    """
    Registra amostra de entrada para análise de drift.
    
    Args:
        payload: Dados da requisição
    """
    try:
        DRIFT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with DRIFT_LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")
    except Exception as e:
        logger.warning(f"Failed to log input sample: {e}")


# Carrega modelo na inicialização do módulo
MODEL = load_model()
