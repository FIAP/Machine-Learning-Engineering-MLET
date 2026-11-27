"""Endpoint de predição de crédito."""

import logging

from fastapi import APIRouter
from pydantic import BaseModel, Field

from src.routes.metrics import increment_request_count
from src.services.model_service import log_input_sample, predict_one

router = APIRouter()
logger = logging.getLogger("credit-api")


class PredictRequest(BaseModel):
    """Schema de requisição para predição."""
    
    age: int = Field(..., description="Idade do cliente", ge=18, le=100)
    income: float = Field(..., description="Renda mensal", gt=0)
    loan_amount: float = Field(..., description="Valor do empréstimo solicitado", gt=0)
    credit_history: str = Field(..., description="Histórico de crédito", pattern="^(good|fair|poor)$")


class PredictResponse(BaseModel):
    """Schema de resposta para predição."""
    
    prediction: str = Field(..., description="Predição: 'approved' ou 'rejected'")
    confidence: float = Field(..., description="Confiança da predição", ge=0, le=1)


@router.post("/predict", response_model=PredictResponse)
def predict_endpoint(payload: PredictRequest):
    """
    Predição de aprovação de crédito.
    
    Args:
        payload: Dados do cliente para predição
        
    Returns:
        PredictResponse: Resultado da predição com confiança
    """
    payload_dict = payload.model_dump()
    
    # Logging e métricas
    logger.info("predict request", extra={"payload": payload_dict})
    increment_request_count()
    log_input_sample(payload_dict)
    
    # Predição
    result = predict_one(payload_dict)
    
    logger.info("predict result", extra={"result": result})
    
    return result
