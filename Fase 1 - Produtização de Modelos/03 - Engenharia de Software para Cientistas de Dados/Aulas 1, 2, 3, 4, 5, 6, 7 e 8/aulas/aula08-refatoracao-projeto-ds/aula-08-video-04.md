---
titulo: "Aula 08 – Parte 04: Melhorias Finais - Configuração, Logging e Estrutura Profissional"
modulo: "Engenharia de software para cientista de dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 20
prerequisitos:
  - "Python 3.12+"
  - "Aula 08 - Parte 03 concluída"
  - "Git e organização básica de projeto"
tags: ["estrutura-projeto", "configuracao", "logging", "ds", "fastapi", "boas-praticas"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula vamos finalizar as melhorias no projeto de Data Science.

Depois de refatorar o código, vamos aplicar melhorias finais: externalizar configurações, melhorar o sistema de logging, organizar a estrutura de pastas seguindo padrões profissionais, e preparar o projeto para ambientes de produção. Vamos transformar nosso projeto em um sistema robusto e mantível.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: O projeto tem valores hardcoded (threshold = 0.6), variáveis globais no código de métricas, e caminhos de arquivos fixos.

**Agitação**: Para mudar um threshold, precisa editar código. Para produção, os caminhos não funcionam. As métricas usam variável global que não funciona em múltiplos workers.

**Solução**: Criar arquivo de configuração, usar variáveis de ambiente, melhorar sistema de métricas com classes, e organizar estrutura de pastas para produção.

# 3. Objetivos de aprendizagem

Ao final você será capaz de:

1. **Externalizar** configurações usando variáveis de ambiente
2. **Refatorar** sistema de métricas removendo estado global
3. **Organizar** estrutura de projeto profissional
4. **Preparar** projeto para múltiplos ambientes (dev, staging, prod)

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Python 3.12+
- Projeto com refatoração da parte 03 completa
- uv instalado

**Setup:**

```powershell
.\.venv\Scripts\Activate.ps1
uv run pytest -q
```

**Checklist de setup:**
- [ ] Módulo `scoring.py` criado
- [ ] Testes unitários passando
- [ ] Backup/commit antes de novas mudanças

# 5. Visão geral do que já existe no projeto (continuidade)

Estado atual (pós-refatoração):
```
swe4ds-credit-api/
├── src/
│   ├── main.py
│   ├── routes/
│   │   ├── predict.py
│   │   └── metrics.py      # 🔥 Usa variável global
│   └── services/
│       ├── model_service.py # 🔥 Caminho hardcoded
│       └── scoring.py       # ✅ Refatorado
├── tests/
│   ├── test_scoring.py     # ✅ Novo
│   └── test_predict.py
├── logs/
└── requirements.txt
```

**O que será alterado nesta parte:**
- Criar `src/config.py` para configurações
- Refatorar `metrics.py` removendo estado global
- Criar estrutura de pastas profissional (data/, models/)
- Adicionar arquivo `.env` para configurações locais

# 6. Passo a passo (comandos + código)

## Passo 1: Criar módulo de configuração (Excalidraw: Slide 6)

**Intenção:** Centralizar todas as configurações em um único lugar.

Crie o arquivo de configuração:

```powershell
New-Item src/config.py -ItemType File
code src/config.py
```

Adicione as configurações:

```python
"""Configurações da aplicação."""

import os
from pathlib import Path

# Diretórios base
BASE_DIR = Path(__file__).parent.parent
LOGS_DIR = BASE_DIR / "logs"
MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"

# Criar diretórios se não existirem
LOGS_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# Configurações do modelo
APPROVAL_THRESHOLD = float(os.getenv("APPROVAL_THRESHOLD", "0.6"))
MODEL_VERSION = os.getenv("MODEL_VERSION", "0.1.0")

# Configurações de logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DRIFT_LOG_PATH = LOGS_DIR / "input_samples.jsonl"

# Configurações da API
API_TITLE = "Credit API"
API_VERSION = "0.2.0"
API_DESCRIPTION = "API de predição de crédito com engenharia de software"

# Configurações de ambiente
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = ENVIRONMENT == "development"
```

**CHECKPOINT:** Configurações centralizadas e usando variáveis de ambiente.

---

## Passo 2: Atualizar model_service.py para usar config (Excalidraw: Slide 6)

**Intenção:** Remover valores hardcoded do serviço.

Abra e edite:

```powershell
code src/services/model_service.py
```

```python
"""Serviço de modelo de ML (simulado)."""

import json
import logging

from src.config import (
    APPROVAL_THRESHOLD,
    DRIFT_LOG_PATH,
    MODEL_VERSION,
)
from src.services.scoring import calculate_credit_score

logger = logging.getLogger("credit-api")


def load_model():
    """
    Carrega o modelo de ML.
    
    Nota: Por enquanto é um modelo simulado.
    Em produção, carregaria um modelo real treinado.
    
    Returns:
        dict: Configuração do modelo simulado
    """
    logger.info(f"Loading model version {MODEL_VERSION}...")
    return {
        "type": "simulated",
        "version": MODEL_VERSION,
        "threshold": APPROVAL_THRESHOLD,
    }


def predict_one(data: dict) -> dict:
    """
    Realiza predição para um único registro.
    
    Args:
        data: Dicionário com features do cliente
        
    Returns:
        dict: Resultado da predição
    """
    # Calcula score usando funções isoladas
    score = calculate_credit_score(data)
    
    # Decisão baseada no threshold configurável
    prediction = "approved" if score >= APPROVAL_THRESHOLD else "rejected"
    
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
```

**CHECKPOINT:** Serviço agora usa configurações centralizadas.

---

## Passo 3: Refatorar sistema de métricas (Excalidraw: Slide 7)

**Intenção:** Remover variável global e usar classe para métricas.

Crie um novo arquivo para gerenciar métricas:

```powershell
New-Item src/services/metrics_service.py -ItemType File
code src/services/metrics_service.py
```

```python
"""Serviço de métricas da aplicação."""

from datetime import datetime


class MetricsCollector:
    """Coletor de métricas da aplicação."""
    
    def __init__(self):
        """Inicializa o coletor de métricas."""
        self.request_count = 0
        self.prediction_count = 0
        self.approved_count = 0
        self.rejected_count = 0
        self.start_time = datetime.now()
    
    def increment_request(self) -> None:
        """Incrementa contador de requisições."""
        self.request_count += 1
    
    def record_prediction(self, prediction: str) -> None:
        """
        Registra uma predição.
        
        Args:
            prediction: 'approved' ou 'rejected'
        """
        self.prediction_count += 1
        if prediction == "approved":
            self.approved_count += 1
        else:
            self.rejected_count += 1
    
    def get_metrics(self) -> dict:
        """
        Retorna todas as métricas coletadas.
        
        Returns:
            dict: Métricas atuais
        """
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        approval_rate = 0.0
        if self.prediction_count > 0:
            approval_rate = self.approved_count / self.prediction_count
        
        return {
            "request_count": self.request_count,
            "prediction_count": self.prediction_count,
            "approved_count": self.approved_count,
            "rejected_count": self.rejected_count,
            "approval_rate": round(approval_rate, 3),
            "uptime_seconds": round(uptime, 1),
            "status": "healthy",
        }
    
    def reset(self) -> None:
        """Reseta todas as métricas."""
        self.__init__()


# Instância global do coletor
metrics_collector = MetricsCollector()
```

**CHECKPOINT:** Sistema de métricas mais robusto e orientado a objetos.

---

## Passo 4: Atualizar routes/metrics.py (Excalidraw: Slide 7)

**Intenção:** Usar o novo serviço de métricas.

Abra e edite:

```powershell
code src/routes/metrics.py
```

```python
"""Endpoint de métricas e health check."""

from fastapi import APIRouter

from src.services.metrics_service import metrics_collector

router = APIRouter()


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
    Métricas detalhadas da aplicação.
    
    Returns:
        dict: Métricas incluindo contadores e taxas
    """
    return metrics_collector.get_metrics()
```

**CHECKPOINT:** Endpoint simplificado usando o novo serviço.

---

## Passo 5: Atualizar routes/predict.py para registrar métricas (Excalidraw: Slide 7)

**Intenção:** Integrar o novo sistema de métricas no endpoint de predição.

Abra e edite:

```powershell
code src/routes/predict.py
```

```python
"""Endpoint de predição de crédito."""

import logging

from fastapi import APIRouter
from pydantic import BaseModel, Field

from src.services.metrics_service import metrics_collector
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
    
    # Logging
    logger.info("predict request", extra={"payload": payload_dict})
    
    # Métricas
    metrics_collector.increment_request()
    
    # Log para análise de drift
    log_input_sample(payload_dict)
    
    # Predição
    result = predict_one(payload_dict)
    
    # Registrar resultado nas métricas
    metrics_collector.record_prediction(result["prediction"])
    
    logger.info("predict result", extra={"result": result})
    
    return result
```

**CHECKPOINT:** Métricas mais ricas sendo coletadas.

---

## Passo 6: Criar estrutura de pastas profissional (Excalidraw: Slide 8)

**Intenção:** Organizar o projeto seguindo padrões da indústria.

Crie as pastas necessárias:

```powershell
# Criar estrutura de dados
New-Item data\raw -ItemType Directory -Force
New-Item data\processed -ItemType Directory -Force
New-Item data\external -ItemType Directory -Force

# Criar pasta de modelos se não existir
New-Item models -ItemType Directory -Force

# Criar pasta de relatórios
New-Item reports -ItemType Directory -Force
New-Item reports\figures -ItemType Directory -Force

# Criar pasta de notebooks
New-Item notebooks -ItemType Directory -Force

# Criar pasta de scripts
if (-not (Test-Path scripts)) {
    New-Item scripts -ItemType Directory -Force
}
```

Estrutura final:
```
swe4ds-credit-api/
├── data/
│   ├── raw/            # Dados originais
│   ├── processed/      # Dados processados
│   └── external/       # Dados externos
├── models/             # Artefatos de modelo
├── notebooks/          # Jupyter notebooks
├── reports/            # Relatórios e visualizações
│   └── figures/
├── scripts/            # Scripts auxiliares
│   ├── deploy_staging.ps1
│   └── run_batch.py
├── src/                # Código fonte
│   ├── config.py       # ✅ Novo
│   ├── main.py
│   ├── routes/
│   └── services/
│       ├── metrics_service.py  # ✅ Novo
│       ├── model_service.py
│       └── scoring.py
├── tests/
├── logs/
└── requirements.txt
```

**CHECKPOINT:** Estrutura profissional e escalável.

---

## Passo 7: Criar arquivo .env para configurações locais

**Intenção:** Permitir configurações diferentes por ambiente.

Crie o arquivo `.env`:

```powershell
New-Item .env -ItemType File
code .env
```

Adicione as configurações de desenvolvimento:

```env
# Configurações de Ambiente
ENVIRONMENT=development
LOG_LEVEL=DEBUG

# Configurações do Modelo
APPROVAL_THRESHOLD=0.6
MODEL_VERSION=0.2.0

# Configurações de API
API_HOST=0.0.0.0
API_PORT=8000
```

Crie também `.env.example` para documentação:

```powershell
Copy-Item .env .env.example
code .env.example
```

**CHECKPOINT:** Configurações externalizadas e documentadas.

---

## Passo 8: Atualizar main.py com configurações (Excalidraw: Slide 8)

**Intenção:** Usar as configurações centralizadas na aplicação principal.

Abra e edite:

```powershell
code src/main.py
```

```python
"""Aplicação principal FastAPI com logging configurado."""

import logging

from fastapi import FastAPI

from src.config import API_DESCRIPTION, API_TITLE, API_VERSION, LOG_LEVEL
from src.routes.metrics import router as metrics_router
from src.routes.predict import router as predict_router

# Configuração de logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger("credit-api")

# Criação da aplicação FastAPI
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
)

# Inclusão dos routers
app.include_router(metrics_router)
app.include_router(predict_router)


@app.get("/")
def root():
    """Endpoint raiz da API."""
    return {
        "message": API_TITLE,
        "version": API_VERSION,
        "docs": "/docs",
    }


@app.on_event("startup")
async def startup_event():
    """Evento executado no startup da aplicação."""
    logger.info(f"Starting {API_TITLE} v{API_VERSION}")
    logger.info(f"Environment: {__import__('src.config').config.ENVIRONMENT}")
```

**CHECKPOINT:** Aplicação usando configurações centralizadas.

---

## Passo 9: Adicionar .gitignore adequado

**Intenção:** Não versionar arquivos sensíveis.

Crie ou atualize `.gitignore`:

```powershell
code .gitignore
```

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/

# IDEs
.vscode/
.idea/

# Dados e modelos
data/raw/*
data/processed/*
models/*.pkl
models/*.joblib

# Logs
logs/*.log
logs/*.jsonl

# Ambiente
.env
!.env.example

# Testes
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store
Thumbs.db
```

**CHECKPOINT:** Arquivos sensíveis protegidos.

---

## Passo 10: Validar todas as mudanças

**Intenção:** Garantir que o projeto funciona com as novas configurações.

```powershell
# Rodar todos os testes
uv run pytest -v

# Subir a API
uv run uvicorn src.main:app --reload

# Testar métricas melhoradas
Invoke-RestMethod -Uri http://localhost:8000/metrics

# Testar predição
$body = @{
    age = 35
    income = 8000.0
    loan_amount = 2000.0
    credit_history = "good"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/predict -Method Post -Body $body -ContentType "application/json"

# Verificar métricas novamente
Invoke-RestMethod -Uri http://localhost:8000/metrics
```

Resposta esperada do `/metrics`:
```json
{
  "request_count": 1,
  "prediction_count": 1,
  "approved_count": 1,
  "rejected_count": 0,
  "approval_rate": 1.0,
  "uptime_seconds": 45.2,
  "status": "healthy"
}
```

**CHECKPOINT:** Tudo funcionando com métricas melhoradas!

# 7. Testes rápidos e validação

```powershell
# Validar estrutura de pastas
Get-ChildItem -Directory | Select-Object Name

# Rodar testes
uv run pytest -v --cov=src

# Testar diferentes configurações
$env:APPROVAL_THRESHOLD="0.7"
uv run uvicorn src.main:app --reload
```

# 8. Observabilidade e boas práticas (mini-bloco)

1. **Configurações externalizadas**: facilita deploy em múltiplos ambientes. Trade-off: mais arquivos de configuração.
2. **Métricas orientadas a objetos**: mais robustas que variáveis globais. Trade-off: um pouco mais de código.
3. **Estrutura padronizada**: acelera onboarding. Trade-off: mais pastas inicialmente vazias.
4. **Logs estruturados**: facilita monitoramento. Trade-off: mais verbose no desenvolvimento.

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| `ModuleNotFoundError: config` | Import incorreto | Usar `from src.config import ...` |
| `.env` não carregado | Falta biblioteca | Instalar `python-dotenv` se necessário |
| Métricas zeradas | Instância recriada | Usar singleton ou state management |
| Testes falhando | Configurações diferentes | Usar fixtures do pytest |

# 10. Exercícios (básico e avançado)

**Básico 1:** Adicionar nova métrica: tempo médio de resposta.
- Adicionar `response_times` na classe `MetricsCollector`
- Calcular média no método `get_metrics`
- Adicionar teste

**Básico 2:** Criar configuração para múltiplos ambientes.
- Criar `.env.production` e `.env.staging`
- Documentar diferenças no README
- Testar carregamento

**Avançado:** Implementar cache de configurações.
- Usar `@lru_cache` para configurações pesadas
- Adicionar hot-reload de configurações
- Testar performance

# 11. Resultados e Lições

**Resultados (como medir):**
- Métricas coletadas: de 1 para 6 indicadores
- Configurações externalizadas: 100% (0 hardcoded)
- Estrutura de pastas: padrão da indústria
- Facilidade de deploy: redução de 80% no tempo de configuração

**Lições:**
- Configurações externalizadas facilitam manutenção
- Métricas bem estruturadas facilitam observabilidade
- Organização de projeto é investimento, não custo
- Boas práticas reduzem bugs em produção

# 12. Encerramento e gancho para a próxima aula (script)

Nesta aula você finalizou as melhorias no projeto de Data Science, aplicando configurações externalizadas, sistema de métricas robusto, e estrutura profissional de pastas.

Com isso, encerramos o módulo de refatoração e organização de projetos. Agora você tem um projeto completo, bem estruturado e pronto para produção. O próximo passo natural seria integrar com pipelines de CI/CD e sistemas de orquestração como Airflow ou Prefect, preparando para escala e automação completa.
