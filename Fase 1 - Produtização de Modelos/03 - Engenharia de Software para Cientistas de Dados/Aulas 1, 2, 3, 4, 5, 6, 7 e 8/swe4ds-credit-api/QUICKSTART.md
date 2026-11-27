# Guia de Início Rápido - SWE-4-DS Credit API

Este guia ajuda você a configurar e executar a aplicação rapidamente.

## Passo 1: Instalação

```bash
# Instalar uv se ainda não tiver
pip install uv

# Instalar dependências
uv pip install -r requirements.txt
```

## Passo 2: Executar a aplicação

```bash
# Rodar a API
uv run uvicorn src.main:app --reload
```

A API estará disponível em: http://localhost:8000

## Passo 3: Testar endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Predição
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d "{\"age\": 30, \"income\": 5000.0, \"loan_amount\": 10000.0, \"credit_history\": \"good\"}"
```

### Métricas
```bash
curl http://localhost:8000/metrics
```

## Passo 4: Rodar testes

```bash
uv run pytest -v
```

## Passo 5: Processamento Batch

```bash
uv run python scripts/run_batch.py
```

## Passo 6: Build Docker (opcional)

```bash
docker build -t credit-api:local .
docker run -p 8000:8000 credit-api:local
```

## Documentação Interativa

Acesse: http://localhost:8000/docs
