"""Aplicação principal FastAPI com logging configurado."""

import logging

from fastapi import FastAPI

from src.routes.metrics import router as metrics_router
from src.routes.predict import router as predict_router

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger("credit-api")

# Criação da aplicação FastAPI
app = FastAPI(
    title="Credit API",
    description="API de predição de crédito para o curso SWE-4-DS",
    version="0.1.0",
)

# Inclusão dos routers
app.include_router(metrics_router)
app.include_router(predict_router)


@app.get("/")
def root():
    """Endpoint raiz da API."""
    return {
        "message": "Credit API",
        "version": "0.1.0",
        "docs": "/docs",
    }
