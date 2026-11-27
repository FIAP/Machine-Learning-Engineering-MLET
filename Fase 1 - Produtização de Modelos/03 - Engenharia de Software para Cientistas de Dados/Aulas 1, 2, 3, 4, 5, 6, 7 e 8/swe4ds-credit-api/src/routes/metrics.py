"""Endpoint de métricas e health check."""

from fastapi import APIRouter

router = APIRouter()

# Contador global de requisições
_request_count = 0


def increment_request_count() -> None:
    """Incrementa o contador de requisições."""
    global _request_count
    _request_count += 1


@router.get("/health")
def health():
    """
    Health check da API.
    
    Returns:
        dict: Status da API
    """
    return {"status": "ok"}


@router.get("/metrics")
def metrics():
    """
    Métricas básicas da aplicação.
    
    Returns:
        dict: Métricas incluindo contadores de requisições
    """
    return {
        "request_count": _request_count,
        "status": "healthy",
    }
