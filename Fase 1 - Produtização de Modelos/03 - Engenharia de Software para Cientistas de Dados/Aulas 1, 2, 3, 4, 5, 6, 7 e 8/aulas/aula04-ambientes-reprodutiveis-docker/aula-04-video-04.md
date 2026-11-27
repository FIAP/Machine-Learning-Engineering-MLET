---
titulo: "Aula 04 – Parte 04: Orquestrando Ambientes - Docker Compose e Boas Práticas"
modulo: "Engenharia de Software para Cientista de Dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 15
prerequisitos:
  - "Python 3.12+"
  - "Docker Desktop instalado"
  - "Aula 04 - Partes 01 a 03 concluídas"
  - "Conhecimento de YAML básico"
tags: ["docker-compose", "orchestration", "security", "best-practices", "yaml"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Essa é a última aula do módulo de Docker, e vamos fechar com uma ferramenta que vai simplificar muito sua vida: o **Docker Compose**.

Até agora, você rodou containers com comandos longos cheios de flags: `-p`, `-v`, `--network`, `--name`. Imagine ter que digitar isso toda vez, ou pior, ter múltiplos containers para subir. Docker Compose resolve isso: você define tudo em um arquivo YAML, e um único comando `docker-compose up` faz a mágica.

Vamos também discutir **boas práticas de segurança** - como versionar imagens, gerenciar secrets, e manter um ambiente seguro. Ao final desta aula, você terá um ambiente completo de desenvolvimento containerizado para o projeto de crédito.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Seu projeto cresceu. Agora você tem a API, um banco de dados para cache, e talvez um serviço de monitoramento. Cada um é um container. Você precisa subir todos na ordem certa, na mesma rede, com os volumes corretos.

**Agitação**: Você cria um script bash com 10 comandos `docker run`. Funciona no seu computador. Passa para o colega, ele esquece de criar a rede antes. Alguém muda a ordem dos comandos e a API tenta conectar no banco que ainda não subiu. O script cresce, fica impossível de manter.

**Solução**: Docker Compose. Um arquivo `docker-compose.yml` define TUDO: serviços, redes, volumes, variáveis de ambiente, dependências. `docker-compose up` sobe tudo na ordem certa. `docker-compose down` para tudo. Reprodutível, versionável, documentado.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Escrever** um arquivo `docker-compose.yml` completo
2. **Definir** múltiplos serviços com suas configurações
3. **Gerenciar** ambientes com comandos do Compose
4. **Aplicar** boas práticas de segurança em containers
5. **Versionar** imagens de forma profissional
6. **Limpar** recursos Docker não utilizados

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Aulas anteriores de Docker concluídas
- Docker Compose instalado (incluído no Docker Desktop)

**Verificar ambiente:**

```bash
# Verificar Docker Compose
docker compose version

# Navegar para o projeto
cd c:\Users\diogomiyake\projects\swe4ds-credit-api

# Garantir que imagem existe
docker images | grep swe4ds-credit-api
```

**Nota**: Versões recentes usam `docker compose` (com espaço). Versões antigas usam `docker-compose` (com hífen). Ambos funcionam.

**Checklist:**
- [ ] Docker Compose disponível
- [ ] Projeto acessível
- [ ] Imagem construída

# 5. Visão geral do que já existe no projeto (continuidade)

**Estado atual:**
```
swe4ds-credit-api/
├── .git/
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── .dockerignore
├── Dockerfile
├── pyproject.toml
├── requirements.txt
├── data/
├── models/
├── scripts/
│   ├── download_data.py
│   └── process_sample.py
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   └── validation.py
└── tests/
    └── ...
```

**O que vamos criar nesta aula:**
```
swe4ds-credit-api/
├── ...
├── docker-compose.yml           # [NOVO] Orquestração
├── docker-compose.dev.yml       # [NOVO] Override para dev
└── .env.example                 # [NOVO] Exemplo de variáveis
```

# 6. Passo a passo (comandos + código)

## Passo 1: Anatomia do docker-compose.yml (Excalidraw: Slide 7)

**Intenção**: Entender a estrutura do arquivo antes de escrever.

### Estrutura Básica

```yaml
# docker-compose.yml

# Versão do formato (opcional em versões recentes)
version: "3.8"

# Serviços (containers)
services:
  nome-servico:
    image: imagem:tag
    # ... configurações

# Redes
networks:
  minha-rede:
    driver: bridge

# Volumes nomeados
volumes:
  meus-dados:
```

### Configurações de Serviço

| Chave | Propósito | Equivalente docker run |
|-------|-----------|----------------------|
| `image` | Imagem a usar | Argumento da imagem |
| `build` | Construir do Dockerfile | `docker build` |
| `ports` | Mapear portas | `-p` |
| `volumes` | Montar volumes | `-v` |
| `environment` | Variáveis de ambiente | `-e` |
| `networks` | Redes a conectar | `--network` |
| `depends_on` | Dependências | (ordem manual) |
| `command` | Sobrescrever CMD | Argumento final |
| `restart` | Política de restart | `--restart` |

**CHECKPOINT**: Você entende a estrutura básica do docker-compose.yml.

---

## Passo 2: Criando docker-compose.yml para o Projeto (Excalidraw: Slide 7)

**Intenção**: Criar configuração completa para desenvolvimento.

Crie `docker-compose.yml`:

```yaml
# docker-compose.yml
# Configuração Docker Compose para swe4ds-credit-api
# Uso: docker compose up

# Define serviços que compõem a aplicação
services:
  
  # ==========================================================================
  # Serviço principal: API de Crédito
  # ==========================================================================
  api:
    # Construir a partir do Dockerfile local
    build:
      context: .
      dockerfile: Dockerfile
    
    # Nome do container
    container_name: credit-api
    
    # Mapear porta 8000 do host para 8000 do container
    ports:
      - "8000:8000"
    
    # Volumes para desenvolvimento
    volumes:
      # Código fonte (hot reload)
      - ./src:/app/src:ro
      # Dados
      - ./data:/app/data
      # Scripts
      - ./scripts:/app/scripts:ro
    
    # Variáveis de ambiente
    environment:
      - PYTHONUNBUFFERED=1
      - ENVIRONMENT=development
      - LOG_LEVEL=DEBUG
    
    # Arquivo de variáveis de ambiente
    env_file:
      - .env
    
    # Rede
    networks:
      - credit-network
    
    # Política de reinício
    restart: unless-stopped
    
    # Health check
    healthcheck:
      test: ["CMD", "python", "-c", "print('healthy')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    
    # Comando padrão (pode ser sobrescrito)
    command: python -c "print('API Credit iniciada! Porta 8000'); import time; time.sleep(3600)"

  # ==========================================================================
  # Serviço de testes
  # ==========================================================================
  tests:
    build:
      context: .
      dockerfile: Dockerfile
    
    container_name: credit-tests
    
    volumes:
      - ./src:/app/src:ro
      - ./tests:/app/tests:ro
    
    environment:
      - PYTHONUNBUFFERED=1
      - ENVIRONMENT=test
    
    networks:
      - credit-network
    
    # Não inicia automaticamente (profile)
    profiles:
      - testing
    
    command: pytest tests/ -v --tb=short

# =============================================================================
# Redes
# =============================================================================
networks:
  credit-network:
    driver: bridge
    name: credit-network

# =============================================================================
# Volumes nomeados (para persistência)
# =============================================================================
volumes:
  credit-data:
    name: credit-data
```

### Explicação das Seções

**Serviço `api`:**
- `build`: Constrói a imagem do Dockerfile local
- `ports`: Mapeia porta 8000
- `volumes`: Monta código e dados (`:ro` = read-only)
- `environment`: Variáveis inline
- `env_file`: Variáveis de arquivo externo
- `healthcheck`: Verifica saúde do serviço

**Serviço `tests`:**
- `profiles`: Só roda quando explicitamente chamado
- Usado para testes isolados

**CHECKPOINT**: `docker-compose.yml` criado.

---

## Passo 3: Arquivo de Variáveis de Ambiente

**Intenção**: Separar configuração do código.

Crie `.env.example`:

```bash
# .env.example
# Copie para .env e configure os valores
# NÃO commite o arquivo .env real!

# Ambiente
ENVIRONMENT=development

# Logging
LOG_LEVEL=INFO

# Dados
DATA_PATH=/app/data
MODEL_PATH=/app/models

# API (para futuro)
API_HOST=0.0.0.0
API_PORT=8000

# Banco de dados (para futuro)
# DATABASE_URL=postgresql://user:pass@db:5432/credit
```

Crie `.env` (não comitar):

```bash
# Copiar exemplo
cp .env.example .env
```

Adicione ao `.gitignore`:

```bash
# Adicionar ao .gitignore
echo ".env" >> .gitignore
```

**CHECKPOINT**: Arquivos de ambiente criados.

---

## Passo 4: Comandos do Docker Compose (Excalidraw: Slide 8)

**Intenção**: Dominar os comandos essenciais.

### Comandos Básicos

```bash
# Subir todos os serviços
docker compose up

# Subir em background (detached)
docker compose up -d

# Subir serviço específico
docker compose up api

# Subir com rebuild da imagem
docker compose up --build

# Ver logs
docker compose logs

# Ver logs de serviço específico
docker compose logs api

# Logs em tempo real
docker compose logs -f

# Parar serviços
docker compose stop

# Parar e remover containers
docker compose down

# Parar, remover e apagar volumes
docker compose down -v
```

### Comandos de Execução

```bash
# Executar comando em serviço rodando
docker compose exec api python --version

# Abrir shell
docker compose exec api bash

# Rodar serviço único (one-off)
docker compose run --rm api python -c "print('Hello')"

# Rodar testes (profile específico)
docker compose --profile testing up tests
```

### Comandos de Gerenciamento

```bash
# Ver status dos serviços
docker compose ps

# Ver configuração resolvida
docker compose config

# Listar imagens usadas
docker compose images

# Ver uso de recursos
docker compose top
```

**CHECKPOINT**: Você conhece os comandos principais do Compose.

---

## Passo 5: Testando a Configuração

**Intenção**: Validar que tudo funciona.

```bash
# Navegar para o projeto
cd c:\Users\diogomiyake\projects\swe4ds-credit-api

# Validar sintaxe do compose file
docker compose config

# Subir serviços (primeira vez demora - build)
docker compose up --build

# Em outro terminal, verificar status
docker compose ps

# Ver logs
docker compose logs api

# Executar comando no container
docker compose exec api python -c "from src.validation import validate_limit_bal; print(validate_limit_bal(50000))"

# Parar
docker compose down
```

**Saída esperada do `docker compose ps`:**
```
NAME          IMAGE                    COMMAND   SERVICE   CREATED   STATUS    PORTS
credit-api    swe4ds-credit-api:...    ...       api       ...       Up        0.0.0.0:8000->8000/tcp
```

**CHECKPOINT**: Serviços sobem e respondem.

---

## Passo 6: Boas Práticas de Segurança (Excalidraw: Slide 8)

**Intenção**: Garantir segurança em ambientes containerizados.

### 1. Nunca Rodar como Root

```dockerfile
# No Dockerfile (já fizemos isso!)
RUN useradd --create-home appuser
USER appuser
```

### 2. Não Expor Secrets no Compose

```yaml
# RUIM: Senha no arquivo
environment:
  - DB_PASSWORD=minhasenha123

# BOM: Usar arquivo .env (não commitado)
env_file:
  - .env

# MELHOR: Usar Docker Secrets (para produção)
secrets:
  db_password:
    file: ./secrets/db_password.txt
```

### 3. Imagens Específicas, Não Latest

```yaml
# RUIM: Pode mudar sem aviso
image: python:latest

# BOM: Versão específica
image: python:3.12-slim
```

### 4. Limitar Recursos

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

### 5. Read-Only Quando Possível

```yaml
volumes:
  - ./src:/app/src:ro  # :ro = read-only
```

### Resumo de Segurança

| Prática | Implementação |
|---------|---------------|
| Usuário não-root | `USER appuser` no Dockerfile |
| Secrets seguros | `.env` local ou Docker Secrets |
| Versões fixas | Tags específicas |
| Recursos limitados | `deploy.resources.limits` |
| Volumes read-only | `:ro` em volumes de código |

**CHECKPOINT**: Você conhece as práticas de segurança essenciais.

---

## Passo 7: Versionamento de Imagens

**Intenção**: Gerenciar versões de forma profissional.

### Estratégia de Tags

```bash
# Versão semântica
docker build -t swe4ds-credit-api:1.0.0 .

# Também marcar como latest
docker tag swe4ds-credit-api:1.0.0 swe4ds-credit-api:latest

# Tag com commit hash (CI/CD)
docker build -t swe4ds-credit-api:$(git rev-parse --short HEAD) .

# Tag com data
docker build -t swe4ds-credit-api:$(date +%Y%m%d) .
```

### No docker-compose.yml

```yaml
services:
  api:
    image: swe4ds-credit-api:${VERSION:-latest}
    build:
      context: .
```

Uso:
```bash
# Usa latest
docker compose up

# Usa versão específica
VERSION=1.0.0 docker compose up
```

### Limpeza de Imagens Antigas

```bash
# Ver todas as imagens do projeto
docker images | grep swe4ds-credit-api

# Remover versões antigas específicas
docker rmi swe4ds-credit-api:0.9.0

# Remover imagens não usadas
docker image prune

# Limpeza geral (cuidado!)
docker system prune -a
```

**CHECKPOINT**: Você sabe versionar e limpar imagens.

---

## Passo 8: Override para Desenvolvimento

**Intenção**: Ter configurações diferentes para dev e prod.

Crie `docker-compose.override.yml`:

```yaml
# docker-compose.override.yml
# Configurações adicionais para desenvolvimento
# Automaticamente carregado junto com docker-compose.yml

services:
  api:
    # Em dev, montar código como volume para hot reload
    volumes:
      - ./src:/app/src
      - ./tests:/app/tests
      - ./scripts:/app/scripts
    
    # Mais variáveis de debug
    environment:
      - DEBUG=true
      - LOG_LEVEL=DEBUG
    
    # Manter container rodando mesmo sem CMD
    stdin_open: true
    tty: true
```

O Docker Compose automaticamente combina `docker-compose.yml` + `docker-compose.override.yml`.

Para produção, use arquivo específico:

```bash
# Produção: ignora override
docker compose -f docker-compose.yml -f docker-compose.prod.yml up
```

**CHECKPOINT**: Você sabe usar overrides para ambientes diferentes.

---

## Passo 9: Commit Final do Módulo

**Intenção**: Versionar toda configuração Docker.

```bash
# Adicionar arquivos
git add Dockerfile .dockerignore docker-compose.yml .env.example

# Commit
git commit -m "feat: adiciona configuração Docker completa

Arquivos adicionados:
- Dockerfile: Imagem Python 3.12-slim otimizada
- .dockerignore: Exclui arquivos desnecessários
- docker-compose.yml: Orquestração de serviços
- .env.example: Template de variáveis de ambiente

Recursos:
- Usuário não-root para segurança
- Health checks configurados
- Volumes para dados e código
- Rede isolada para serviços"

# Push
git push origin main
```

**CHECKPOINT**: Configuração Docker versionada.

# 7. Testes rápidos e validação

```bash
# Validar compose file
docker compose config

# Subir em background
docker compose up -d

# Verificar status
docker compose ps

# Testar execução
docker compose exec api python -c "import sys; print(f'Python {sys.version}')"

# Ver logs
docker compose logs api | tail -10

# Rodar testes (se profile configurado)
docker compose --profile testing run --rm tests

# Limpar
docker compose down
```

# 8. Observabilidade e boas práticas (mini-bloco)

### Boas Práticas Consolidadas

1. **Um serviço por container**
   - Cada container faz uma coisa
   - Facilita escalonamento e manutenção
   - **Trade-off**: Mais containers para gerenciar

2. **Compose para desenvolvimento**
   - Ambiente reprodutível com um comando
   - Override para customizações locais
   - **Trade-off**: Kubernetes pode ser melhor para produção

3. **Volumes nomeados para persistência**
   - `volumes:` no compose para dados importantes
   - Sobrevive a `docker compose down`
   - **Trade-off**: Precisa limpar manualmente

4. **Health checks em todos os serviços**
   - Docker sabe se serviço está saudável
   - Permite restart automático
   - **Trade-off**: Mais configuração

5. **Logging centralizado**
   - `docker compose logs` para todos os serviços
   - Considere driver de log (json-file, syslog)
   - **Trade-off**: Pode precisar de solução externa

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| `yaml syntax error` | Indentação errada | Use 2 espaços, não tabs |
| `service not found` | Nome errado | Verifique `services:` no yml |
| `port already allocated` | Porta em uso | Mude a porta ou pare o processo |
| `volume mount denied` | Permissão do Docker | Compartilhe drive no Docker Desktop |
| `network not found` | Rede não criada | `docker compose up` cria automaticamente |
| Serviço não inicia | Dependência não pronta | Use `depends_on` com `condition` |

# 10. Exercícios (básico e avançado)

## Exercício Básico 1: Adicionar Serviço de Notebook

Adicione um serviço Jupyter Notebook ao compose que:
- Use imagem `jupyter/scipy-notebook`
- Exponha porta 8888
- Monte a pasta `data/` como volume

**Critério de sucesso**: Acessar Jupyter em http://localhost:8888

## Exercício Básico 2: Health Check Customizado

Crie um script `healthcheck.py` que verifica se os módulos principais podem ser importados. Configure o health check no compose para usar esse script.

**Critério de sucesso**: `docker compose ps` mostra status "healthy"

## Exercício Avançado: Ambiente Multi-Serviço

Crie um ambiente com:
1. API (seu código)
2. PostgreSQL (banco de dados)
3. Redis (cache)

Configure as conexões via variáveis de ambiente.

**Critério de sucesso**: API conecta em ambos os serviços.

# 11. Resultados e Lições

## Métricas do Módulo

| Métrica | Início | Fim |
|---------|--------|-----|
| Docker instalado | Não | Sim |
| Dockerfile criado | - | Otimizado |
| Compose configurado | - | Completo |
| Segurança | - | Não-root, secrets |
| Versionamento | - | Tags semânticas |

## Lições do Módulo de Docker

1. **"Funciona na minha máquina"** → Docker resolve
2. **Dockerfile** é receita executável
3. **docker-compose** simplifica multi-container
4. **Volumes** persistem dados
5. **Redes** conectam serviços
6. **Segurança** começa com usuário não-root

## Comandos Essenciais

```bash
# Build
docker build -t app:v1 .

# Run
docker run -d -p 8000:8000 -v ./data:/data app:v1

# Compose
docker compose up -d
docker compose down
docker compose logs -f

# Limpeza
docker system prune -a
```

# 12. Encerramento e gancho para a próxima aula (script)

Parabéns! Você completou o módulo de Docker e Containerização. Em 4 aulas você aprendeu:

- Por que containers são essenciais para reprodutibilidade
- Como escrever Dockerfiles otimizados
- Como executar containers com portas, volumes e redes
- Como orquestrar ambientes com Docker Compose

Seu projeto agora tem um ambiente de desenvolvimento completamente containerizado. Qualquer pessoa pode clonar o repositório, rodar `docker compose up`, e ter tudo funcionando. Isso é profissional.

Na próxima aula, vamos mudar de assunto e falar sobre **Gerenciamento de Dependências**. Você vai aprender sobre ambientes virtuais Python em profundidade, ferramentas como Poetry e UV, e como publicar seu código como um pacote reutilizável.

O container está pronto. Agora vamos garantir que as dependências dentro dele também sejam gerenciadas corretamente. Até a próxima aula!
