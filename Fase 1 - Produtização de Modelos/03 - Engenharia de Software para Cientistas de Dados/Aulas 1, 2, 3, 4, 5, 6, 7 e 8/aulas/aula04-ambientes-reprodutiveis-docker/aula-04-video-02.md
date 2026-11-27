---
titulo: "Aula 04 – Parte 02: Criando Imagens - Dockerfile Passo a Passo em Projeto de DS"
modulo: "Engenharia de Software para Cientista de Dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 25
prerequisitos:
  - "Python 3.12+"
  - "Docker Desktop instalado e rodando"
  - "Aula 04 - Parte 01 concluída"
  - "Repositório swe4ds-credit-api"
tags: ["docker", "dockerfile", "build", "imagem", "data-science"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula, vamos criar nosso primeiro **Dockerfile** do zero. Na aula anterior, entendemos a teoria de containerização. Agora vamos transformar essa teoria em prática.

O Dockerfile é como uma receita: uma lista de instruções que o Docker segue para construir uma imagem. Cada linha adiciona uma camada à imagem final. Vamos aprender as instruções essenciais - FROM, COPY, RUN, CMD - e aplicá-las para containerizar nossa API de crédito.

Ao final desta aula, você terá uma imagem Docker funcional do seu projeto. Uma imagem que pode ser executada em qualquer máquina com Docker instalado, garantindo a reprodutibilidade que discutimos.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Você quer compartilhar seu projeto de ML com a equipe de produção. Eles pedem um "container". Você nunca escreveu um Dockerfile. Olha exemplos na internet, cada um diferente do outro. Copia um, tenta adaptar, não funciona. Erros misteriosos durante o build.

**Agitação**: Você perde horas debugando. O container fica gigante (2GB). O build demora 10 minutos a cada mudança. Você não entende por que algumas coisas funcionam e outras não. A equipe de DevOps reclama da imagem mal otimizada. O deploy é bloqueado.

**Solução**: Aprender Dockerfile do zero, entendendo cada instrução. Aplicar boas práticas desde o início: imagem base adequada, multi-stage builds, cache de camadas, .dockerignore. Resultado: imagem leve, build rápido, deploy aprovado. Vamos construir isso juntos para a API de crédito.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Escrever** um Dockerfile completo para projeto Python
2. **Escolher** a imagem base adequada para Data Science
3. **Utilizar** instruções FROM, WORKDIR, COPY, RUN, ENV, EXPOSE, CMD
4. **Construir** uma imagem Docker com `docker build`
5. **Aplicar** boas práticas para imagens eficientes (cache, .dockerignore)
6. **Verificar** que a imagem funciona corretamente

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Aula 04 - Parte 01 concluída
- Docker Desktop rodando
- Repositório `swe4ds-credit-api` atualizado

**Verificar ambiente:**

```bash
# Navegar para o projeto
cd c:\Users\diogomiyake\projects\swe4ds-credit-api

# Ativar ambiente virtual
.venv\Scripts\activate

# Verificar Docker
docker --version
docker info | head -5

# Verificar estrutura do projeto
ls -la
```

**Checklist:**
- [ ] Docker rodando
- [ ] Projeto acessível
- [ ] requirements.txt atualizado

# 5. Visão geral do que já existe no projeto (continuidade)

**Estado atual:**
```
swe4ds-credit-api/
├── .git/
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── .venv/
├── pyproject.toml
├── requirements.txt
├── data/
│   ├── raw/
│   └── processed/
├── models/
├── scripts/
│   └── download_data.py
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   └── validation.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── unit/
        ├── __init__.py
        ├── test_data_loader.py
        └── test_validation.py
```

**O que vamos criar nesta aula:**
```
swe4ds-credit-api/
├── ...
├── Dockerfile                   # [NOVO] Definição da imagem
└── .dockerignore                # [NOVO] Arquivos a ignorar no build
```

# 6. Passo a passo (comandos + código)

## Passo 1: Anatomia de um Dockerfile (Excalidraw: Slide 3)

**Intenção**: Entender a estrutura antes de escrever.

### Estrutura Básica

```dockerfile
# Comentário: Linhas começando com # são ignoradas

# FROM: Define a imagem base
FROM python:3.12-slim

# WORKDIR: Define o diretório de trabalho dentro do container
WORKDIR /app

# COPY: Copia arquivos do host para o container
COPY requirements.txt .

# RUN: Executa comandos durante o build
RUN pip install -r requirements.txt

# COPY: Copia o resto do código
COPY . .

# ENV: Define variáveis de ambiente
ENV PYTHONUNBUFFERED=1

# EXPOSE: Documenta a porta que a aplicação usa
EXPOSE 8000

# CMD: Comando padrão ao iniciar o container
CMD ["python", "app.py"]
```

### Instruções Principais

| Instrução | Propósito | Exemplo |
|-----------|-----------|---------|
| `FROM` | Imagem base | `FROM python:3.12-slim` |
| `WORKDIR` | Diretório de trabalho | `WORKDIR /app` |
| `COPY` | Copiar arquivos | `COPY . .` |
| `RUN` | Executar comando | `RUN pip install pandas` |
| `ENV` | Variável de ambiente | `ENV DEBUG=false` |
| `EXPOSE` | Documentar porta | `EXPOSE 8000` |
| `CMD` | Comando padrão | `CMD ["python", "main.py"]` |
| `ENTRYPOINT` | Comando fixo | `ENTRYPOINT ["python"]` |
| `ARG` | Argumento de build | `ARG VERSION=1.0` |

### Camadas (Layers)

Cada instrução cria uma **camada**. O Docker faz cache de camadas:

```
┌─────────────────────────────────────────────────────────────────┐
│                    CAMADAS DA IMAGEM                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FROM python:3.12-slim     ─────►  Camada base (150MB)         │
│                                         │                       │
│  RUN pip install...        ─────►  Camada deps (200MB)         │
│                                         │                       │
│  COPY . .                  ─────►  Camada código (5MB)         │
│                                         │                       │
│                                    ═════════════                │
│                                    IMAGEM FINAL                 │
│                                    (~355MB)                     │
│                                                                 │
│  Se você mudar só o código, Docker reusa cache das deps!       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**CHECKPOINT**: Você entende que cada instrução cria uma camada?

---

## Passo 2: Escolhendo a Imagem Base (Excalidraw: Slide 3 - Imagem Base)

**Intenção**: Selecionar a base certa para projetos de Data Science.

### Opções de Imagem Python

| Imagem | Tamanho | Prós | Contras |
|--------|---------|------|---------|
| `python:3.12` | ~900MB | Tudo incluído | Muito grande |
| `python:3.12-slim` | ~150MB | Equilibrado | Faltam algumas libs |
| `python:3.12-alpine` | ~50MB | Muito leve | Incompatível com muitas libs DS |

### Por que NÃO usar Alpine para Data Science?

Alpine usa `musl libc` em vez de `glibc`. Muitas bibliotecas de Data Science (numpy, pandas, scipy) são compiladas para glibc e precisam ser recompiladas para Alpine, o que:
- Demora muito (build de 20+ minutos)
- Pode falhar
- Imagem final fica maior que slim!

**Recomendação para DS**: Use `python:3.12-slim`

### Verificar Tamanhos

```bash
# Baixar imagens para comparar
docker pull python:3.12
docker pull python:3.12-slim
docker pull python:3.12-alpine

# Comparar tamanhos
docker images | grep python
```

**Saída típica:**
```
python     3.12         abc123   900MB
python     3.12-slim    def456   150MB
python     3.12-alpine  ghi789    50MB
```

**CHECKPOINT**: Você sabe por que `slim` é melhor que `alpine` para DS.

---

## Passo 3: Criando o Dockerfile da API de Crédito (Excalidraw: Slide 4)

**Intenção**: Escrever o Dockerfile completo para nosso projeto.

### Atualizar requirements.txt

Primeiro, garanta que o requirements.txt está atualizado:

```bash
# Ativar ambiente
.venv\Scripts\activate

# Atualizar requirements
uv pip freeze > requirements.txt

# Verificar conteúdo
cat requirements.txt
```

### Criar o Dockerfile

Crie o arquivo `Dockerfile` na raiz do projeto:

```dockerfile
# Dockerfile
# Imagem Docker para API de Análise de Crédito
# Projeto: swe4ds-credit-api
# Versão: 1.0

# =============================================================================
# ESTÁGIO 1: Imagem Base
# =============================================================================
FROM python:3.12-slim

# Metadados da imagem
LABEL maintainer="seu-email@exemplo.com"
LABEL version="1.0"
LABEL description="API de predição de inadimplência de cartão de crédito"

# =============================================================================
# CONFIGURAÇÃO DO AMBIENTE
# =============================================================================

# Variáveis de ambiente Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Diretório de trabalho
WORKDIR /app

# =============================================================================
# INSTALAÇÃO DE DEPENDÊNCIAS DO SISTEMA
# =============================================================================

# Instalar dependências do sistema (necessárias para algumas libs Python)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# =============================================================================
# INSTALAÇÃO DE DEPENDÊNCIAS PYTHON
# =============================================================================

# Copiar apenas requirements primeiro (para cache de camadas)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# =============================================================================
# CÓPIA DO CÓDIGO DA APLICAÇÃO
# =============================================================================

# Copiar código fonte
COPY src/ ./src/

# Copiar outros arquivos necessários
COPY pyproject.toml .

# =============================================================================
# CONFIGURAÇÃO FINAL
# =============================================================================

# Criar usuário não-root para segurança
RUN useradd --create-home --shell /bin/bash appuser
RUN chown -R appuser:appuser /app
USER appuser

# Porta que a aplicação vai usar (documentação)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando padrão (será sobrescrito quando tivermos FastAPI)
CMD ["python", "-c", "print('Container swe4ds-credit-api iniciado!')"]
```

### Explicação Detalhada

**Seção 1 - Imagem Base:**
```dockerfile
FROM python:3.12-slim
```
- Usa Python 3.12 em Debian slim (leve mas compatível)

**Seção 2 - Variáveis de Ambiente:**
```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
```
- `PYTHONDONTWRITEBYTECODE=1`: Não gera arquivos `.pyc`
- `PYTHONUNBUFFERED=1`: Output imediato (importante para logs)

**Seção 3 - Dependências do Sistema:**
```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
```
- Instala compiladores (necessários para algumas libs)
- `--no-install-recommends`: Não instala pacotes sugeridos
- Remove cache do apt para reduzir tamanho

**Seção 4 - Dependências Python:**
```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```
- Copia requirements ANTES do código (cache!)
- Se código mudar mas deps não, Docker usa cache

**Seção 5 - Código:**
```dockerfile
COPY src/ ./src/
```
- Copia apenas o necessário

**Seção 6 - Segurança:**
```dockerfile
RUN useradd --create-home --shell /bin/bash appuser
USER appuser
```
- Não roda como root (segurança)

**CHECKPOINT**: Dockerfile criado com todas as seções.

---

## Passo 4: Criando o .dockerignore (Excalidraw: Slide 4 - Boas Práticas)

**Intenção**: Evitar copiar arquivos desnecessários para a imagem.

Crie `.dockerignore` na raiz:

```text
# .dockerignore
# Arquivos e pastas a ignorar durante docker build

# Ambiente virtual Python
.venv/
venv/
env/
__pycache__/
*.py[cod]
*$py.class
*.so

# Testes (não vão para produção)
tests/
pytest_cache/
.pytest_cache/
htmlcov/
.coverage
coverage.xml

# Git
.git/
.gitignore

# IDE
.vscode/
.idea/
*.swp
*.swo

# Docker
Dockerfile
docker-compose*.yml
.dockerignore

# Dados (serão montados via volume)
data/
*.csv
*.parquet

# Modelos (serão montados via volume ou baixados)
models/
*.pkl
*.joblib

# DVC
.dvc/
dvc.lock
*.dvc

# Documentação
docs/
*.md
!README.md

# Outros
.env
.env.*
*.log
tmp/
temp/
```

### Por que .dockerignore é Importante?

```
┌─────────────────────────────────────────────────────────────────┐
│                    COM vs SEM .dockerignore                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SEM .dockerignore:                                             │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  COPY . .  copia TUDO:                                   │   │
│  │  - .venv/ (500MB)                                        │   │
│  │  - .git/ (50MB)                                          │   │
│  │  - data/ (1GB)                                           │   │
│  │  - models/ (200MB)                                       │   │
│  │  - tests/ (desnecessário em prod)                        │   │
│  │                                                          │   │
│  │  Resultado: Imagem de 2GB+, build lento                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  COM .dockerignore:                                             │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  COPY . .  copia apenas código:                          │   │
│  │  - src/ (5MB)                                            │   │
│  │  - pyproject.toml                                        │   │
│  │                                                          │   │
│  │  Resultado: Imagem de ~400MB, build rápido               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**CHECKPOINT**: `.dockerignore` criado.

---

## Passo 5: Construindo a Imagem (docker build)

**Intenção**: Criar a imagem a partir do Dockerfile.

### Comando docker build

```bash
# Navegar para o diretório do projeto
cd c:\Users\diogomiyake\projects\swe4ds-credit-api

# Construir imagem
docker build -t swe4ds-credit-api:v1.0 .
```

**Explicação dos parâmetros:**
- `-t swe4ds-credit-api:v1.0`: Tag da imagem (nome:versão)
- `.`: Contexto de build (diretório atual)

### Output Esperado

```
[+] Building 45.3s (14/14) FINISHED
 => [internal] load build definition from Dockerfile
 => [internal] load .dockerignore
 => [internal] load metadata for docker.io/library/python:3.12-slim
 => [1/9] FROM docker.io/library/python:3.12-slim
 => [2/9] WORKDIR /app
 => [3/9] RUN apt-get update && apt-get install -y ...
 => [4/9] COPY requirements.txt .
 => [5/9] RUN pip install --no-cache-dir -r requirements.txt
 => [6/9] COPY src/ ./src/
 => [7/9] COPY pyproject.toml .
 => [8/9] RUN useradd --create-home --shell /bin/bash appuser
 => [9/9] RUN chown -R appuser:appuser /app
 => exporting to image
 => => naming to docker.io/library/swe4ds-credit-api:v1.0
```

### Verificar Imagem Criada

```bash
# Listar imagens
docker images | grep swe4ds

# Ver detalhes
docker inspect swe4ds-credit-api:v1.0 | head -50

# Ver histórico de camadas
docker history swe4ds-credit-api:v1.0
```

**Saída esperada de `docker images`:**
```
REPOSITORY          TAG    IMAGE ID       CREATED          SIZE
swe4ds-credit-api   v1.0   abc123def456   2 minutes ago    ~400MB
```

**CHECKPOINT**: Imagem criada com sucesso (verificar com `docker images`).

---

## Passo 6: Testando a Imagem

**Intenção**: Verificar que a imagem funciona corretamente.

### Executar Container

```bash
# Rodar container
docker run --rm swe4ds-credit-api:v1.0
```

**Saída esperada:**
```
Container swe4ds-credit-api iniciado!
```

### Explorar o Container

```bash
# Entrar no container interativamente
docker run -it --rm swe4ds-credit-api:v1.0 bash

# Dentro do container:
pwd                    # /app
ls -la                 # Ver arquivos
python --version       # Python 3.12.x
pip list | head -10    # Ver pacotes instalados
whoami                 # appuser (não root!)
exit
```

### Verificar Módulo src

```bash
# Testar import do módulo
docker run --rm swe4ds-credit-api:v1.0 \
    python -c "from src.validation import validate_limit_bal; print(validate_limit_bal(50000))"
```

**Saída esperada:**
```
True
```

**CHECKPOINT**: Container executa e imports funcionam.

---

## Passo 7: Otimizando o Build (Cache de Camadas)

**Intenção**: Entender e aproveitar o cache do Docker.

### Demonstração do Cache

```bash
# Primeiro build (sem cache)
docker build -t swe4ds-credit-api:v1.0 . --no-cache
# Demora ~45 segundos

# Segundo build (com cache, sem mudanças)
docker build -t swe4ds-credit-api:v1.0 .
# Demora ~2 segundos (usa cache!)

# Modificar um arquivo Python
echo "# comment" >> src/validation.py

# Terceiro build
docker build -t swe4ds-credit-api:v1.0 .
# Demora ~5 segundos (reusa cache das deps, só recopia código)

# Reverter mudança
git checkout src/validation.py
```

### Ordem das Instruções Importa!

```dockerfile
# RUIM: Qualquer mudança no código invalida cache das deps
COPY . .
RUN pip install -r requirements.txt

# BOM: Mudança no código NÃO invalida cache das deps
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

**CHECKPOINT**: Você entende como a ordem das instruções afeta o cache.

---

## Passo 8: Commit do Dockerfile

**Intenção**: Versionar os arquivos Docker.

```bash
# Adicionar arquivos
git add Dockerfile .dockerignore

# Commit
git commit -m "feat: adiciona Dockerfile para containerização

- Usa python:3.12-slim como base
- Configura usuário não-root para segurança
- Adiciona .dockerignore para builds eficientes
- Inclui healthcheck para monitoramento"

# Push (se desejar)
# git push origin main
```

**CHECKPOINT**: Dockerfile versionado no Git.

# 7. Testes rápidos e validação

```bash
# Verificar imagem existe
docker images | grep swe4ds-credit-api

# Verificar container roda
docker run --rm swe4ds-credit-api:v1.0

# Verificar módulo importa
docker run --rm swe4ds-credit-api:v1.0 \
    python -c "from src.data_loader import get_feature_names; print('OK')"

# Verificar usuário não-root
docker run --rm swe4ds-credit-api:v1.0 whoami
# Esperado: appuser
```

# 8. Observabilidade e boas práticas (mini-bloco)

### Boas Práticas Aplicadas

1. **Imagem base slim**
   - `python:3.12-slim` é leve mas compatível
   - Reduz tamanho da imagem e superfície de ataque
   - **Trade-off**: Pode precisar instalar algumas libs do sistema

2. **Usuário não-root**
   - Container não roda como root
   - Limita danos se container for comprometido
   - **Trade-off**: Pode ter problemas de permissão em alguns cenários

3. **Cache de camadas otimizado**
   - requirements.txt copiado antes do código
   - Mudanças no código não invalidam cache de deps
   - **Trade-off**: Dockerfile mais longo

4. **Variáveis de ambiente para Python**
   - `PYTHONUNBUFFERED=1` para logs imediatos
   - `PYTHONDONTWRITEBYTECODE=1` para imagem menor
   - **Trade-off**: Nenhum significativo

5. **.dockerignore bem configurado**
   - Exclui venv, dados, testes
   - Build mais rápido e imagem menor
   - **Trade-off**: Precisa manter atualizado

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| `COPY failed: file not found` | Arquivo no .dockerignore | Remova do .dockerignore |
| `pip install failed` | Falta dependência do sistema | Adicione ao apt-get install |
| Build muito lento | Cache invalidado | Verifique ordem das instruções |
| Imagem muito grande | Arquivos desnecessários | Verifique .dockerignore |
| `Permission denied` | Arquivos de outro owner | Use `chown` antes de `USER` |
| `ModuleNotFoundError` | Estrutura de COPY errada | Verifique paths no COPY |

# 10. Exercícios (básico e avançado)

## Exercício Básico 1: Adicionar Dependência

Adicione `httpx` ao requirements.txt, rebuilde a imagem e verifique que foi instalado:

```bash
# 1. Adicionar httpx ao requirements.txt
# 2. Rebuild
docker build -t swe4ds-credit-api:v1.1 .
# 3. Verificar
docker run --rm swe4ds-credit-api:v1.1 pip show httpx
```

**Critério de sucesso**: `pip show httpx` mostra informações do pacote.

## Exercício Básico 2: Customizar CMD

Modifique o CMD para executar um script Python específico. Crie `src/healthcheck.py` que imprime informações do sistema.

**Critério de sucesso**: Container executa o script e mostra versão Python + pacotes principais.

## Exercício Avançado: Multi-stage Build

Pesquise e implemente um Dockerfile multi-stage que:
1. Estágio 1 (builder): Instala dependências e compila
2. Estágio 2 (runtime): Apenas copia o necessário

**Critério de sucesso**: Imagem final menor que a versão atual.

# 11. Resultados e Lições

## Métricas Finais

| Métrica | Como Medir | Valor Esperado |
|---------|------------|----------------|
| Imagem criada | `docker images` | Listada |
| Tamanho | `docker images` | ~400MB |
| Tempo de build (cache) | Observar | < 5s |
| Container executa | `docker run` | Sem erros |
| Usuário não-root | `whoami` | appuser |

## Lições Aprendidas

1. **Dockerfile é uma receita** - sequência de instruções para construir imagem
2. **Ordem importa para cache** - coloque o que muda menos primeiro
3. **.dockerignore é essencial** - exclua arquivos desnecessários
4. **Use slim, não alpine** - para projetos de Data Science
5. **Não rode como root** - crie usuário dedicado

# 12. Encerramento e gancho para a próxima aula (script)

Excelente trabalho! Você acabou de criar seu primeiro Dockerfile completo para um projeto de Data Science. A imagem está pronta, otimizada, e segura.

Você aprendeu cada instrução do Dockerfile, entendeu como o cache funciona, e aplicou boas práticas desde o início. Seu projeto agora tem uma forma padronizada de ser executado em qualquer lugar.

Na próxima aula, vamos colocar essa imagem para rodar de verdade. Vamos aprender sobre `docker run` em detalhes: como mapear portas, montar volumes para dados, e fazer containers se comunicarem. Você vai ver seu código executando dentro do container, acessando dados do host, e respondendo requisições.

Prepare-se para a parte mais interativa! Até a próxima aula.
