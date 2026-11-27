# SWE-4-DS Credit API

API de predição de crédito para o curso de Engenharia de Software para Cientistas de Dados.

## Requisitos

- Python 3.12+
- uv (gerenciador de pacotes)

## Instalação

```bash
# Criar ambiente virtual e instalar dependências
uv sync

# Ativar ambiente virtual (Windows)
.\.venv\Scripts\Activate.ps1
```

## Execução

```bash
# Rodar API localmente
uv run uvicorn src.main:app --reload

# Rodar testes
uv run pytest -q

# Rodar lint
uv run ruff check src/ tests/
```

## Docker

### Construir a imagem

```bash
# Construir imagem Docker
docker build -t swe4ds-credit-api:latest .

# Construir com tag específica
docker build -t swe4ds-credit-api:v1.0.0 .
```

### Executar o container

```bash
# Rodar container em modo interativo
docker run -p 8000:8000 swe4ds-credit-api:latest

# Rodar container em background (detached)
docker run -d -p 8000:8000 --name credit-api swe4ds-credit-api:latest

# Rodar com variáveis de ambiente
docker run -p 8000:8000 -e LOG_LEVEL=debug swe4ds-credit-api:latest
```

### Testar a API no container

```bash
# Verificar saúde da API
curl http://localhost:8000/health

# Fazer uma predição
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d "{\"features\": [1.0, 2.0, 3.0]}"

# Ver métricas
curl http://localhost:8000/metrics

# Acessar documentação interativa
# Abra no navegador: http://localhost:8000/docs
```

### Gerenciar containers

```bash
# Listar containers em execução
docker ps

# Ver logs do container
docker logs credit-api

# Parar container
docker stop credit-api

# Remover container
docker rm credit-api

# Remover imagem
docker rmi swe4ds-credit-api:latest
```

## Endpoints

- `GET /health` - Verifica saúde da API
- `POST /predict` - Predição de crédito
- `GET /metrics` - Métricas da aplicação

## CI/CD

O projeto possui pipeline de CI/CD configurado no GitHub Actions que executa:
- Lint com Ruff
- Testes automatizados
- Build do container Docker
- Deploy em staging (simulado)
