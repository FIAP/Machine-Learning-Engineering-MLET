---
titulo: "Aula 07 – Parte 03: Monitoramento de Modelos e Aplicações de DS em Produção"
modulo: "Engenharia de software para cientista de dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 25
prerequisitos:
  - "Python 3.12+"
  - "FastAPI com endpoint de predição"
  - "Conceitos básicos de logging"
tags: ["monitoramento", "observabilidade", "metrics", "drift", "fastapi"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula vamos falar sobre **monitoramento** e **observabilidade** em aplicações de Data Science.

Quando colocamos um modelo em produção, o trabalho não termina. A performance pode cair, o comportamento dos dados pode mudar e o usuário percebe antes de você. Monitorar sistemas e modelos é o que garante que a API continue confiável.

Vamos ver métricas de sistema, métricas de aplicação e métricas específicas de modelos — como drift — sempre conectando com a API que já estamos construindo. Ao final, você terá um caminho prático para acompanhar o que acontece depois do deploy.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Seu modelo estava bom no treinamento, mas meses depois a acurácia em produção caiu.

**Agitação**: Ninguém percebeu, a taxa de erro subiu e decisões erradas foram tomadas. Quando descobriram, o dano já estava feito.

**Solução**: Monitoramento contínuo. Coletar métricas de sistema (CPU, memória), aplicação (latência, throughput) e modelo (distribuição dos dados e performance). Tudo integrado à API que estamos evoluindo.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Definir** métricas de sistema e aplicação relevantes
2. **Instrumentar** logs e métricas básicas em FastAPI
3. **Detectar** sinais de drift em dados de entrada
4. **Planejar** alertas para cenários críticos

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Python 3.12+
- FastAPI rodando localmente
- Dependências de logging já instaladas

**Setup:**

```bash
# Ativar ambiente
.\.venv\Scripts\Activate.ps1

# Rodar API local
uv run uvicorn src.main:app --reload
```

**Checklist de setup:**
- [ ] API ativa em http://localhost:8000
- [ ] Endpoint /health respondendo
- [ ] Acesso ao modelo em Consumer_API

# 5. Visão geral do que já existe no projeto (continuidade)

Estado atual esperado:
```
swe4ds-credit-api/
├── src/
│   ├── main.py
│   ├── routes/
│   │   └── predict.py
│   └── services/
│       └── model_service.py
└── tests/
```

**O que será alterado nesta parte:**
- Adicionar logging estruturado
- Criar endpoint simples de métricas
- Registrar dados de entrada para análise de drift

# 6. Passo a passo (comandos + código)

## Passo 1: Logging estruturado (Excalidraw: Slide 3)

**Intenção:** Registrar eventos críticos de predição.

Arquivo: `src/main.py` (trecho a adicionar — diff lógico)

```python
# (ADICIONAR no topo do arquivo, junto aos imports)
import logging
```

```python
# (ADICIONAR após criação do app)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger("credit-api")
```

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger("credit-api")
```

Arquivo: `src/routes/predict.py` (trecho a adicionar — diff lógico)

```python
from src.main import logger

@router.post("/predict")
def predict_endpoint(payload: PredictRequest):
    logger.info("predict request", extra={"payload": payload.model_dump()})
    result = predict_one(MODEL, payload.model_dump())
    logger.info("predict result", extra={"result": result})
    return {"prediction": result}
```

**CHECKPOINT:** Ao chamar `/predict`, você verá logs no console.

---

## Passo 2: Endpoint simples de métricas

**Intenção:** Expor métricas básicas para observabilidade.

Arquivo: `src/routes/metrics.py` (novo — criar arquivo)

```bash
New-Item src/routes/metrics.py -ItemType File
code src/routes/metrics.py
```

```python
from fastapi import APIRouter

router = APIRouter()

_request_count = 0


def increment_request_count() -> None:
    global _request_count
    _request_count += 1


@router.get("/metrics")
def metrics():
    return {"request_count": _request_count}


@router.get("/health")
def health():
    return {"status": "ok"}
```

Arquivo: `src/main.py` (trecho a adicionar — diff lógico)

```python
from src.routes.metrics import router as metrics_router

app.include_router(metrics_router)
```

**CHECKPOINT:** Acessar `/metrics` deve retornar JSON com contador.

---

## Passo 3: Registrar dados para análise de drift (Excalidraw: Slide 5)

**Intenção:** Armazenar entradas para comparação futura.

Arquivo: `src/services/model_service.py` (trecho a adicionar — diff lógico)

```python
import json
from pathlib import Path

DRIFT_LOG_PATH = Path("logs/input_samples.jsonl")


def log_input_sample(payload: dict) -> None:
    DRIFT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DRIFT_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")
```

Arquivo: `src/routes/predict.py` (trecho a adicionar — diff lógico)

```python
from src.routes.metrics import increment_request_count
from src.services.model_service import log_input_sample

@router.post("/predict")
def predict_endpoint(payload: PredictRequest):
    payload_dict = payload.model_dump()
    increment_request_count()
    log_input_sample(payload_dict)
    result = predict_one(MODEL, payload_dict)
    return {"prediction": result}
```

**CHECKPOINT:** Após algumas requisições, `logs/input_samples.jsonl` deve existir.

---

## Passo 4: Métricas de modelo (exemplo conceitual)

**Intenção:** Mostrar como medir performance do modelo.

Exemplo de avaliação offline (placeholder):

```python
from sklearn.metrics import accuracy_score

# y_true e y_pred obtidos do histórico real
acc = accuracy_score(y_true, y_pred)
print("accuracy:", acc)
```

**CHECKPOINT:** Métrica calculada quando houver dados rotulados.

---

## Passo 5: Teste automatizado de métricas

**Intenção:** Garantir que o endpoint `/metrics` responde corretamente.

Arquivo: `tests/test_metrics.py` (novo)

```bash
New-Item tests/test_metrics.py -ItemType File
code tests/test_metrics.py
```

```python
"""Testes básicos para o endpoint de métricas."""

from fastapi.testclient import TestClient

from src.main import app


def test_metrics_endpoint_returns_counter():
    client = TestClient(app)
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "request_count" in response.json()
```

```bash
uv run pytest tests/test_metrics.py -v
```

**CHECKPOINT:** Teste de métricas passa localmente.

# 7. Testes rápidos e validação

```bash
# Testar health
curl http://localhost:8000/health

# Testar predict
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d "{\"age\": 30, \"limit\": 2000, \"history\": \"good\"}"

# Windows
Invoke-WebRequest -Uri "http://localhost:8000/predict" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"age": 30, "income": 5000, "loan_amount": 2000, "credit_history": "good"}' | Select-Object -Expand Content

# Rejected
Invoke-WebRequest -Uri "http://localhost:8000/predict" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"age": 70, "income": 3000, "loan_amount": 10000, "credit_history": "poor"}' | Select-Object -Expand Content

# Testar metrics
curl http://localhost:8000/metrics
```

Resposta esperada (exemplo):
```json
{"request_count": 3}
```

Teste automatizado simples:

```python
def test_metrics(client):
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "request_count" in r.json()
```

# 8. Observabilidade e boas práticas (mini-bloco)

1. **Logs estruturados**: facilitam análise e debugging. Trade-off: mais volume de logs.
2. **Métricas expostas**: permitem dashboards e alertas. Trade-off: manter endpoints seguros.
3. **Registro de amostras**: base para drift. Trade-off: cuidado com privacidade e compliance.

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| `/metrics` não responde | Router não incluído | Verificar `include_router` |
| Logs não aparecem | Logger não configurado | Revisar `logging.basicConfig` |
| Arquivo de drift não criado | Permissões | Criar pasta `logs/` |
| Alta latência | Logging excessivo | Reduzir nível ou amostrar logs |

# 10. Exercícios (básico e avançado)

**Básico 1:** Adicionar contagem por endpoint (ex: `/predict`).
- Concluído com sucesso: contadores separados por rota.

**Básico 2:** Registrar tempo de resposta no log.
- Concluído com sucesso: log inclui duração em ms.

**Avançado:** Criar script que compare distribuição de `age` no treino vs produção.
- Concluído com sucesso: relatório simples de drift (ex: histogramas).

# 11. Resultados e Lições

**Resultados (como medir):**
- Latência média (calcular a partir dos logs)
- Taxa de erro (contar respostas não-2xx)
- Drift de dados (comparar distribuições em amostras)

**Lições:**
- Monitoramento é parte do ciclo de vida do modelo
- Logs e métricas dão visibilidade real
- Drift não é bug, é fenômeno esperado

# 12. Encerramento e gancho para a próxima aula (script)

Nesta aula você aprendeu a monitorar sua API e seu modelo, com logs estruturados, métricas básicas e preparação para detecção de drift.

Na próxima parte, vamos juntar tudo em um **pipeline completo de CI/CD**, com build de container, deploy em staging e coleta de logs e métricas. Vamos fechar o ciclo do commit até a operação monitorada.
