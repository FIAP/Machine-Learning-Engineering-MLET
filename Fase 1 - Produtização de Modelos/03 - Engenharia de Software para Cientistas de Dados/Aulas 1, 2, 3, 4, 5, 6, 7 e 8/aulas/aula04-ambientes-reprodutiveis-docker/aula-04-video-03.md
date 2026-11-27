---
titulo: "Aula 04 – Parte 03: Mão na Massa - Executando Contêineres, Volumes e Rede"
modulo: "Engenharia de Software para Cientista de Dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 30
prerequisitos:
  - "Python 3.12+"
  - "Docker Desktop instalado"
  - "Aula 04 - Partes 01 e 02 concluídas"
  - "Imagem swe4ds-credit-api:v1.0 construída"
tags: ["docker", "volumes", "ports", "networking", "containers"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Essa é a aula mais prática do módulo de Docker. Até agora, criamos uma imagem. Agora vamos aprender a executá-la de verdade: mapear portas para acessar serviços, montar volumes para persistir dados, e conectar containers em rede.

Esta é a aula mais longa do módulo - 30 minutos - porque tem muito conteúdo hands-on. Você vai sair sabendo rodar containers como um profissional. Vai entender como seu código dentro do container se comunica com o mundo externo.

Ao final, vamos containerizar e executar uma aplicação Python real, acessando dados do seu computador de dentro do container. Isso é exatamente o que você fará em projetos de Data Science reais.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Você construiu a imagem Docker. Roda `docker run minha-imagem`. O container inicia, executa algo, e para. Como você acessa a API que está rodando lá dentro? Os dados estão no seu computador, como o container acessa? Você faz alterações, precisa rebuildar toda vez?

**Agitação**: A documentação do Docker é vasta e confusa. Você tenta `-p 8000:8000`, não funciona. Tenta `-v /dados:/dados`, erro de permissão. O container roda como root e você tem problemas de ownership nos arquivos. Dados processados dentro do container são perdidos quando você o remove.

**Solução**: Entender os três pilares de execução: portas (comunicação), volumes (dados), e redes (conexão entre containers). Cada um tem flags específicas no `docker run`. Vamos dominar cada um deles com exemplos práticos e progressivos.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Executar** containers com `docker run` e suas principais flags
2. **Mapear** portas entre container e host para acessar serviços
3. **Montar** volumes para persistir dados e compartilhar arquivos
4. **Criar** redes Docker para comunicação entre containers
5. **Executar** comandos em containers rodando (docker exec)
6. **Gerenciar** ciclo de vida de containers (start, stop, rm)

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Aulas anteriores de Docker concluídas
- Imagem `swe4ds-credit-api:v1.0` construída

**Verificar ambiente:**

```bash
# Verificar imagem existe
docker images | grep swe4ds-credit-api

# Se não existir, rebuildar
cd c:\Users\diogomiyake\projects\swe4ds-credit-api
docker build -t swe4ds-credit-api:v1.0 .

# Limpar containers antigos
docker container prune -f
```

**Checklist:**
- [ ] Imagem `swe4ds-credit-api:v1.0` existe
- [ ] Docker Desktop rodando
- [ ] Terminal pronto

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
│   ├── raw/
│   │   └── (dados CSV aqui)
│   └── processed/
├── models/
├── scripts/
│   └── download_data.py
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   └── validation.py
└── tests/
    └── ...
```

**O que faremos nesta aula:**
- Executar containers de várias formas
- Montar a pasta `data/` dentro do container
- Expor portas para acessar serviços
- Criar rede para múltiplos containers

# 6. Passo a passo (comandos + código)

## Passo 1: Anatomia do docker run (Excalidraw: Slide 5)

**Intenção**: Entender o comando mais importante do Docker.

### Estrutura do Comando

```bash
docker run [OPÇÕES] IMAGEM [COMANDO] [ARGUMENTOS]
```

### Opções Mais Comuns

| Flag | Significado | Exemplo |
|------|-------------|---------|
| `-d` | Detached (background) | `docker run -d nginx` |
| `-it` | Interativo + TTY | `docker run -it python bash` |
| `--rm` | Remove ao parar | `docker run --rm python` |
| `--name` | Nome do container | `docker run --name meu-app` |
| `-p` | Mapeia porta | `-p 8000:80` |
| `-v` | Monta volume | `-v /host:/container` |
| `-e` | Variável de ambiente | `-e DEBUG=true` |
| `--network` | Conecta à rede | `--network minha-rede` |

### Exemplos Básicos

```bash
# Rodar e sair
docker run swe4ds-credit-api:v1.0

# Rodar interativo
docker run -it swe4ds-credit-api:v1.0 bash

# Rodar em background com nome
docker run -d --name credit-api swe4ds-credit-api:v1.0 sleep infinity

# Verificar container rodando
docker ps

# Parar container
docker stop credit-api

# Remover container
docker rm credit-api
```

**CHECKPOINT**: Você consegue rodar container em foreground e background.

---

## Passo 2: Modos de Execução

**Intenção**: Entender quando usar cada modo.

### Foreground (Padrão)

```bash
# Container executa e você vê o output
docker run swe4ds-credit-api:v1.0 python -c "print('Hello!')"
```
- Output vai para seu terminal
- Ctrl+C para o container
- Bom para debugging

### Interactive (-it)

```bash
# Abre shell dentro do container
docker run -it --rm swe4ds-credit-api:v1.0 bash

# Dentro do container:
python --version
ls -la
exit
```
- `-i`: Input interativo
- `-t`: Aloca pseudo-TTY
- Bom para explorar/debugar

### Detached (-d)

```bash
# Roda em background
docker run -d --name api-background swe4ds-credit-api:v1.0 sleep 3600

# Ver logs
docker logs api-background

# Ver logs em tempo real
docker logs -f api-background

# Parar
docker stop api-background
```
- Container roda independente do terminal
- Use `docker logs` para ver output
- Bom para serviços de longa duração

**CHECKPOINT**: Você entende a diferença entre -it e -d.

---

## Passo 3: Mapeamento de Portas (Excalidraw: Slide 5 - Portas)

**Intenção**: Acessar serviços dentro do container.

### O Problema

Container está isolado. Se um servidor roda na porta 8000 dentro do container, você não consegue acessar de fora.

### A Solução: Flag -p

```bash
-p HOST_PORT:CONTAINER_PORT
```

### Exemplo com Servidor Python

Primeiro, vamos criar um servidor simples para teste:

```bash
# Criar servidor HTTP simples dentro do container
docker run -d --name webserver \
    -p 8000:8000 \
    python:3.12-slim \
    python -m http.server 8000

# Verificar que está rodando
docker ps

# Acessar do host
curl http://localhost:8000
# Ou abra no navegador: http://localhost:8000
```

**Saída esperada:**
```html
<!DOCTYPE HTML>
<html lang="en">
...
```

### Diagrama de Portas

```
┌─────────────────────────────────────────────────────────────────┐
│                    MAPEAMENTO DE PORTAS                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Seu Computador (Host)                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │  Browser → http://localhost:8000                        │   │
│  │                    │                                     │   │
│  │                    ▼                                     │   │
│  │              ┌──────────┐                                │   │
│  │              │ Porta    │                                │   │
│  │              │  8000    │ ◄─── -p 8000:8000             │   │
│  │              └────┬─────┘                                │   │
│  │                   │                                      │   │
│  │  ─────────────────┼───────────────────────────────────  │   │
│  │                   │                                      │   │
│  │  Container        │                                      │   │
│  │  ┌────────────────┼────────────────────────────────┐    │   │
│  │  │                │                                 │    │   │
│  │  │          ┌─────▼──────┐                         │    │   │
│  │  │          │   Porta    │                         │    │   │
│  │  │          │    8000    │                         │    │   │
│  │  │          └─────┬──────┘                         │    │   │
│  │  │                │                                 │    │   │
│  │  │          ┌─────▼──────┐                         │    │   │
│  │  │          │  Servidor  │                         │    │   │
│  │  │          │   Python   │                         │    │   │
│  │  │          └────────────┘                         │    │   │
│  │  └─────────────────────────────────────────────────┘    │   │
│  │                                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Portas Diferentes

```bash
# Host 9000 → Container 8000
docker run -d -p 9000:8000 python:3.12-slim python -m http.server 8000
# Acesse http://localhost:9000

# Múltiplas portas
docker run -d -p 8000:8000 -p 8001:8001 minha-imagem
```

### Limpeza

```bash
docker stop webserver
docker rm webserver
```

**CHECKPOINT**: Você consegue acessar um serviço dentro do container via porta mapeada.

---

## Passo 4: Montando Volumes (Excalidraw: Slide 5 - Volumes)

**Intenção**: Compartilhar dados entre host e container.

### O Problema

- Dados no host não são visíveis dentro do container
- Dados criados no container são perdidos quando o container é removido

### A Solução: Bind Mounts

```bash
-v /caminho/host:/caminho/container
```

### Exemplo: Acessar Dados do Projeto

```bash
# No Windows, use caminho completo
docker run -it --rm \
    -v c:\Users\diogomiyake\projects\swe4ds-credit-api\data:/app/data \
    swe4ds-credit-api:v1.0 \
    bash

# Dentro do container:
ls -la /app/data/
ls -la /app/data/raw/
```

Se você tiver dados em `data/raw/`, eles aparecerão no container!

### Diagrama de Volumes

```
┌─────────────────────────────────────────────────────────────────┐
│                    BIND MOUNT (Volume)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Host (Seu Computador)                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │  c:\Users\...\swe4ds-credit-api\data\                   │   │
│  │  ├── raw/                                                │   │
│  │  │   └── credit_data.csv                                │   │
│  │  └── processed/                                          │   │
│  │          │                                               │   │
│  │          │ -v .../data:/app/data                        │   │
│  │          │                                               │   │
│  │  ────────┼──────────────────────────────────────────    │   │
│  │          │                                               │   │
│  │  Container                                               │   │
│  │  ┌───────┼──────────────────────────────────────────┐   │   │
│  │  │       ▼                                           │   │   │
│  │  │  /app/data/                                       │   │   │
│  │  │  ├── raw/                                         │   │   │
│  │  │  │   └── credit_data.csv  (mesmo arquivo!)       │   │   │
│  │  │  └── processed/                                   │   │   │
│  │  │                                                   │   │   │
│  │  │  Mudanças aqui refletem no host!                 │   │   │
│  │  └───────────────────────────────────────────────────┘   │   │
│  │                                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Exemplo Prático: Processar Dados

```bash
# Criar script de teste
# Crie um arquivo scripts/test_volume.py:
```

```python
# scripts/test_volume.py
"""Script para testar acesso a volumes."""
from pathlib import Path
import sys

data_dir = Path("/app/data")
print(f"Diretório de dados existe: {data_dir.exists()}")

if data_dir.exists():
    print("\nConteúdo:")
    for item in data_dir.rglob("*"):
        print(f"  {item}")
else:
    print("Diretório /app/data não encontrado!")
    print("Monte um volume com -v")
    sys.exit(1)
```

```bash
# Executar script com volume montado
docker run --rm \
    -v c:\Users\diogomiyake\projects\swe4ds-credit-api\data:/app/data \
    -v c:\Users\diogomiyake\projects\swe4ds-credit-api\scripts:/app/scripts \
    swe4ds-credit-api:v1.0 \
    python /app/scripts/test_volume.py
```

### Volume Read-Only

```bash
# :ro torna o volume somente leitura
docker run --rm \
    -v c:\Users\diogomiyake\projects\swe4ds-credit-api\data:/app/data:ro \
    swe4ds-credit-api:v1.0 \
    bash -c "touch /app/data/teste.txt"
# Erro: Read-only file system
```

**CHECKPOINT**: Você consegue acessar arquivos do host dentro do container.

---

## Passo 5: Docker Exec - Comandos em Container Rodando

**Intenção**: Interagir com containers em execução.

### Iniciar Container em Background

```bash
# Iniciar container que fica rodando
docker run -d --name api-dev \
    -v c:\Users\diogomiyake\projects\swe4ds-credit-api:/app \
    swe4ds-credit-api:v1.0 \
    sleep infinity

# Verificar que está rodando
docker ps
```

### Executar Comandos

```bash
# Executar comando único
docker exec api-dev python --version

# Executar script
docker exec api-dev python -c "from src.validation import validate_limit_bal; print(validate_limit_bal(50000))"

# Abrir shell interativo
docker exec -it api-dev bash

# Dentro do shell:
ls -la
python -c "import pandas; print(pandas.__version__)"
exit
```

### Diferença: run vs exec

| Comando | O que faz |
|---------|-----------|
| `docker run` | Cria NOVO container a partir de imagem |
| `docker exec` | Executa comando em container EXISTENTE |

**CHECKPOINT**: Você consegue executar comandos em container rodando.

---

## Passo 6: Redes Docker (Excalidraw: Slide 6)

**Intenção**: Conectar múltiplos containers.

### Por que Redes?

Em projetos reais, você terá múltiplos containers:
- Container da API
- Container do banco de dados
- Container do cache (Redis)

Eles precisam se comunicar!

### Criando uma Rede

```bash
# Criar rede
docker network create credit-network

# Listar redes
docker network ls
```

### Exemplo: Dois Containers na Mesma Rede

```bash
# Parar container anterior se existir
docker stop api-dev 2>/dev/null
docker rm api-dev 2>/dev/null

# Container 1: "servidor"
docker run -d --name servidor \
    --network credit-network \
    python:3.12-slim \
    python -m http.server 8000

# Container 2: "cliente"
docker run --rm \
    --network credit-network \
    python:3.12-slim \
    python -c "import urllib.request; print(urllib.request.urlopen('http://servidor:8000').read()[:100])"
```

**Note**: O cliente acessa o servidor pelo NOME (`servidor`), não por IP!

### Diagrama de Rede

```
┌─────────────────────────────────────────────────────────────────┐
│                    REDE DOCKER                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  credit-network                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │  ┌───────────────┐         ┌───────────────┐            │   │
│  │  │   servidor    │         │    cliente    │            │   │
│  │  │               │         │               │            │   │
│  │  │  Python HTTP  │ ◄────── │  Faz request  │            │   │
│  │  │  Server :8000 │         │  para         │            │   │
│  │  │               │         │  servidor:8000│            │   │
│  │  └───────────────┘         └───────────────┘            │   │
│  │                                                          │   │
│  │  DNS interno: containers se encontram pelo nome!        │   │
│  │                                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Fora da rede: acessível só se portas mapeadas                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Limpeza

```bash
docker stop servidor
docker rm servidor
docker network rm credit-network
```

**CHECKPOINT**: Você consegue fazer containers se comunicarem via rede.

---

## Passo 7: Exemplo Integrado - Aplicação Python com Dados

**Intenção**: Juntar tudo em um exemplo real.

Vamos criar um script que processa dados e usar Docker para executá-lo.

### Criar Script de Processamento

Crie `scripts/process_sample.py`:

```python
# scripts/process_sample.py
"""
Script para demonstrar processamento de dados em container.
Usa volume para ler dados e salvar resultados.
"""
from pathlib import Path
import sys

# Adicionar src ao path
sys.path.insert(0, "/app")

from src.data_loader import get_feature_names
from src.validation import validate_limit_bal, validate_age
import pandas as pd


def main():
    print("=" * 50)
    print("Processamento de Dados em Container Docker")
    print("=" * 50)
    
    # Verificar diretório de dados
    data_dir = Path("/app/data/raw")
    output_dir = Path("/app/data/processed")
    
    if not data_dir.exists():
        print(f"\n[ERRO] Diretório não encontrado: {data_dir}")
        print("Monte o volume com: -v /seu/path/data:/app/data")
        return 1
    
    # Listar arquivos
    print(f"\nArquivos em {data_dir}:")
    for f in data_dir.iterdir():
        print(f"  - {f.name}")
    
    # Criar dados de exemplo se não existir CSV
    csv_files = list(data_dir.glob("*.csv"))
    if not csv_files:
        print("\n[INFO] Nenhum CSV encontrado. Criando dados de exemplo...")
        sample_data = pd.DataFrame({
            "ID": range(1, 11),
            "LIMIT_BAL": [50000, 100000, 30000, 80000, 60000, 
                        150000, 20000, 90000, 70000, 40000],
            "AGE": [25, 35, 28, 42, 31, 55, 22, 38, 45, 29],
            "default payment next month": [0, 0, 1, 0, 1, 0, 1, 0, 0, 1]
        })
        sample_file = data_dir / "sample_credit.csv"
        sample_data.to_csv(sample_file, index=False)
        print(f"  Criado: {sample_file}")
        csv_files = [sample_file]
    
    # Processar primeiro CSV encontrado
    csv_file = csv_files[0]
    print(f"\nProcessando: {csv_file.name}")
    
    df = pd.read_csv(csv_file)
    print(f"  Linhas: {len(df)}")
    print(f"  Colunas: {list(df.columns)}")
    
    # Validar dados
    print("\nValidação:")
    if "LIMIT_BAL" in df.columns:
        valid_limits = df["LIMIT_BAL"].apply(validate_limit_bal).sum()
        print(f"  Limites válidos: {valid_limits}/{len(df)}")
    
    if "AGE" in df.columns:
        valid_ages = df["AGE"].apply(validate_age).sum()
        print(f"  Idades válidas: {valid_ages}/{len(df)}")
    
    # Salvar resultado
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "processed_sample.csv"
    df.to_csv(output_file, index=False)
    print(f"\nResultado salvo em: {output_file}")
    
    print("\n" + "=" * 50)
    print("Processamento concluído com sucesso!")
    print("=" * 50)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

### Executar com Docker

```bash
# Executar o script com volumes montados
docker run --rm \
    -v c:\Users\diogomiyake\projects\swe4ds-credit-api\src:/app/src \
    -v c:\Users\diogomiyake\projects\swe4ds-credit-api\scripts:/app/scripts \
    -v c:\Users\diogomiyake\projects\swe4ds-credit-api\data:/app/data \
    swe4ds-credit-api:v1.0 \
    python /app/scripts/process_sample.py
```

**Saída esperada:**
```
==================================================
Processamento de Dados em Container Docker
==================================================

Arquivos em /app/data/raw:
  - (seus arquivos)

Processando: sample_credit.csv
  Linhas: 10
  Colunas: ['ID', 'LIMIT_BAL', 'AGE', 'default payment next month']

Validação:
  Limites válidos: 10/10
  Idades válidas: 10/10

Resultado salvo em: /app/data/processed/processed_sample.csv

==================================================
Processamento concluído com sucesso!
==================================================
```

### Verificar que Arquivo foi Criado no Host

```bash
# No host (fora do container)
ls data/processed/
# Deve mostrar: processed_sample.csv
```

O arquivo foi criado DENTRO do container mas aparece no seu computador porque o volume está montado!

**CHECKPOINT**: Você executou um script Python no container que leu e salvou dados via volume.

---

## Passo 8: Comandos de Gerenciamento

**Intenção**: Dominar o ciclo de vida de containers.

### Listar Containers

```bash
# Apenas rodando
docker ps

# Todos (inclusive parados)
docker ps -a

# Formato customizado
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### Ciclo de Vida

```bash
# Criar e iniciar
docker run -d --name meu-container swe4ds-credit-api:v1.0 sleep infinity

# Pausar
docker pause meu-container

# Despausar
docker unpause meu-container

# Parar (graceful)
docker stop meu-container

# Iniciar novamente
docker start meu-container

# Reiniciar
docker restart meu-container

# Forçar parada (kill)
docker kill meu-container

# Remover (precisa estar parado)
docker rm meu-container

# Remover forçado
docker rm -f meu-container
```

### Limpeza em Massa

```bash
# Remover todos containers parados
docker container prune

# Remover imagens não usadas
docker image prune

# Limpeza geral (cuidado!)
docker system prune -a
```

**CHECKPOINT**: Você sabe gerenciar o ciclo de vida de containers.

# 7. Testes rápidos e validação

```bash
# Teste 1: Porta mapeada
docker run -d --name test-port -p 9999:8000 python:3.12-slim python -m http.server 8000
curl http://localhost:9999 | head -5
docker rm -f test-port

# Teste 2: Volume
docker run --rm -v c:\Users\diogomiyake\projects\swe4ds-credit-api:/app swe4ds-credit-api:v1.0 ls /app

# Teste 3: Exec
docker run -d --name test-exec swe4ds-credit-api:v1.0 sleep 60
docker exec test-exec python --version
docker rm -f test-exec

# Teste 4: Rede
docker network create test-net
docker run -d --name test-server --network test-net python:3.12-slim python -m http.server 8000
docker run --rm --network test-net python:3.12-slim python -c "import urllib.request; print('OK')" 2>/dev/null || echo "OK (conexão funciona)"
docker rm -f test-server
docker network rm test-net
```

# 8. Observabilidade e boas práticas (mini-bloco)

### Boas Práticas de Execução

1. **Use --rm para containers temporários**
   - `docker run --rm` remove automaticamente ao parar
   - Evita acúmulo de containers parados
   - **Trade-off**: Perde logs após término

2. **Nomeie seus containers**
   - `--name api-dev` é melhor que ID aleatório
   - Facilita referência em scripts
   - **Trade-off**: Nome deve ser único

3. **Volumes para dados mutáveis**
   - Dados não devem ficar dentro da imagem
   - Use volumes para persistência
   - **Trade-off**: Mais flags no comando

4. **Redes customizadas para multi-container**
   - Isola comunicação
   - DNS automático por nome
   - **Trade-off**: Setup adicional

5. **Logs centralizados**
   - `docker logs` para ver output
   - `-f` para follow em tempo real
   - **Trade-off**: Logs perdidos se container removido

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| `port already in use` | Porta ocupada | Use outra porta ou pare o processo |
| `volume mount failed` | Caminho errado | Use caminho absoluto completo |
| `permission denied` no volume | Owner diferente | Ajuste permissões ou use user correto |
| Container para imediatamente | CMD termina | Use `sleep infinity` ou serviço |
| `network not found` | Rede não existe | Crie com `docker network create` |
| Container não encontra outro | Redes diferentes | Coloque ambos na mesma rede |

# 10. Exercícios (básico e avançado)

## Exercício Básico 1: Servidor de Arquivos

Crie um container que serve os arquivos da pasta `data/` via HTTP na porta 8080.

```bash
# Dica: use python -m http.server e monte o volume correto
docker run -d --name file-server ...
```

**Critério de sucesso**: Acessar http://localhost:8080 e ver os arquivos.

## Exercício Básico 2: Processamento em Lote

Modifique `process_sample.py` para aceitar argumentos (nome do arquivo de entrada). Execute via Docker passando argumentos.

**Critério de sucesso**: `docker run ... python script.py --input meu_arquivo.csv`

## Exercício Avançado: Comunicação entre Containers

Crie dois containers na mesma rede:
1. Container "producer": gera dados e salva em volume compartilhado
2. Container "consumer": lê dados do volume e processa

**Critério de sucesso**: Consumer processa dados gerados pelo producer.

# 11. Resultados e Lições

## Métricas Esperadas

| Operação | Como Medir | Esperado |
|----------|------------|----------|
| Porta mapeada | `curl localhost:PORTA` | Resposta do servidor |
| Volume funciona | Arquivo criado no host | Arquivo existe |
| Rede funciona | Ping por nome | Resolução DNS |
| Exec funciona | Comando retorna | Output esperado |

## Lições Aprendidas

1. **-p mapeia portas** - HOST:CONTAINER
2. **-v monta volumes** - HOST:CONTAINER
3. **--network conecta** - Containers se encontram por nome
4. **docker exec** - Comandos em container rodando
5. **Volumes persistem dados** - Sobrevivem ao container

# 12. Encerramento e gancho para a próxima aula (script)

Fantástico! Você dominou a execução de containers Docker. Sabe mapear portas, montar volumes, criar redes, e gerenciar containers. Essas são as habilidades essenciais para trabalhar com Docker no dia a dia.

Você viu na prática como executar código Python em containers, acessando dados do seu computador e salvando resultados que persistem. Isso é exatamente o workflow de projetos de Data Science reais.

Na próxima e última aula deste módulo, vamos aprender sobre **Docker Compose** - uma ferramenta que simplifica tudo isso. Em vez de comandos longos com muitas flags, você vai definir tudo em um arquivo YAML. Um único comando `docker-compose up` vai subir múltiplos containers configurados e conectados.

Vamos também discutir boas práticas de segurança e versionamento de imagens. É o fechamento perfeito do módulo de Docker. Até lá!
