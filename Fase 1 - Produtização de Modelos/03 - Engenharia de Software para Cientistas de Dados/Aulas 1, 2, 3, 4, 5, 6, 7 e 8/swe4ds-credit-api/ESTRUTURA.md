# Resumo da Estrutura - Aula 07

Esta estrutura foi criada para suportar os vídeos 1-4 da Aula 07.

## Estrutura Criada

```
swe4ds-credit-api/
├── .github/
│   └── workflows/
│       ├── ci.yml              # Pipeline de CI básico
│       └── cicd.yml            # Pipeline completo CI/CD
├── logs/
│   └── .gitkeep                # Mantém diretório no git
├── scripts/
│   ├── deploy_staging.ps1      # Script de deploy simulado
│   └── run_batch.py            # Processamento batch
├── src/
│   ├── __init__.py
│   ├── main.py                 # Aplicação FastAPI principal
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── metrics.py          # Endpoints de health e métricas
│   │   └── predict.py          # Endpoint de predição
│   └── services/
│       ├── __init__.py
│       └── model_service.py    # Lógica de predição (simulada)
├── tests/
│   ├── __init__.py
│   ├── test_health.py          # Testes de health check
│   ├── test_metrics.py         # Testes de métricas
│   └── test_predict.py         # Testes de predição
├── .gitignore
├── Dockerfile                  # Container da aplicação
├── pyproject.toml              # Configuração do projeto
├── requirements.txt            # Dependências
├── README.md                   # Documentação principal
└── QUICKSTART.md               # Guia rápido de início
```

## Mapeamento para os Vídeos

### Vídeo 01 - CI
- `.github/workflows/ci.yml` - Pipeline básico
- `tests/` - Testes automatizados
- Valida: lint + testes

### Vídeo 02 - Estratégias de Deploy
- `scripts/run_batch.py` - Exemplo de batch
- `src/routes/predict.py` - API tempo real
- Demonstra: batch vs real-time

### Vídeo 03 - Monitoramento
- `src/routes/metrics.py` - Endpoint de métricas
- `src/services/model_service.py` - Log de amostras para drift
- `logs/` - Armazenamento de logs

### Vídeo 04 - Pipeline Completo
- `.github/workflows/cicd.yml` - Pipeline completo
- `scripts/deploy_staging.ps1` - Deploy automatizado
- `Dockerfile` - Containerização

## Features Implementadas

✅ API FastAPI funcional com:
   - Health check (`/health`)
   - Predição de crédito (`/predict`)
   - Métricas básicas (`/metrics`)

✅ Modelo de ML simulado com lógica de regras

✅ Logging estruturado

✅ Métricas e contadores de requisições

✅ Log de amostras para análise de drift

✅ Testes automatizados completos

✅ Pipeline CI/CD no GitHub Actions

✅ Dockerfile para containerização

✅ Script de deploy simulado

✅ Processamento batch

## Como Usar

1. **Instalar dependências:**
   ```bash
   pip install uv
   uv pip install -r requirements.txt
   ```

2. **Rodar localmente:**
   ```bash
   uv run uvicorn src.main:app --reload
   ```

3. **Rodar testes:**
   ```bash
   uv run pytest -v
   ```

4. **Testar endpoint:**
   ```bash
   curl -X POST http://localhost:8000/predict \
     -H "Content-Type: application/json" \
     -d "{\"age\": 30, \"income\": 5000.0, \"loan_amount\": 10000.0, \"credit_history\": \"good\"}"
   ```

5. **Processar batch:**
   ```bash
   uv run python scripts/run_batch.py
   ```

## Notas Importantes

- O modelo é **simulado** com regras simples
- O deploy é **simulado** (não sobe container real)
- Logs são salvos em `logs/input_samples.jsonl`
- Métricas são armazenadas em memória (reiniciam ao reiniciar a API)

## Próximos Passos

Para uso em produção, considere:
- Integrar modelo real treinado
- Configurar registry de containers
- Adicionar autenticação nos endpoints
- Implementar métricas persistentes (Prometheus)
- Configurar alertas
- Adicionar testes de integração
