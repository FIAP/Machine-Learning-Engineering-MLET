---
titulo: "Aula 04 – Parte 01: Por que Contêineres? Conceitos de Docker para Reprodutibilidade"
modulo: "Engenharia de Software para Cientista de Dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 20
prerequisitos:
  - "Python 3.12+"
  - "UV instalado"
  - "Aula 03 concluída (testes automatizados)"
  - "Repositório swe4ds-credit-api com CI configurado"
tags: ["docker", "containers", "reproducibility", "devops", "data-science"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula, vamos resolver um dos problemas mais frustrantes em projetos de Data Science: o famoso **"funciona na minha máquina"**. Quem nunca ouviu isso? Você desenvolve um modelo, treina, testa, funciona perfeitamente. Passa para o colega ou para produção e... quebra.

Hoje vamos entender **Docker** e **containerização** - a tecnologia que revolucionou como entregamos software. Com Docker, seu código, dependências e ambiente ficam empacotados juntos. Se roda no seu notebook, roda no servidor, roda na nuvem. Garantido.

Esta é uma aula mais teórica, mas fundamental. Precisamos entender os conceitos antes de colocar a mão na massa. Na próxima aula, vamos criar nosso primeiro Dockerfile para a API de crédito.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Você desenvolveu um modelo de Machine Learning incrível. Funciona perfeitamente no seu Jupyter Notebook com Python 3.12, scikit-learn 1.5, pandas 2.2. Você faz commit, manda para o colega reproduzir. Ele tem Python 3.10, scikit-learn 1.2, e um pandas antigo. O código quebra com erros misteriosos.

**Agitação**: Você passa horas debugando. Descobre que é incompatibilidade de versões. Atualiza as libs dele, mas agora outro projeto dele quebra. Você documenta todas as versões no README, mas ninguém lê. Chega o deploy: o servidor de produção tem Linux, você desenvolveu no Windows. Mais incompatibilidades. A equipe de DevOps reclama. O modelo que era "pronto" leva semanas para entrar em produção.

**Solução**: Docker empacota tudo: sistema operacional base, Python, bibliotecas, seu código. O que roda no container do seu notebook é **exatamente** o que roda em produção. Não existe "mas na minha máquina funciona" porque o container É a máquina. Vamos aprender a containerizar nossa API de crédito para garantir reprodutibilidade total.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Explicar** o problema de reprodutibilidade em projetos de Data Science
2. **Diferenciar** contêineres de máquinas virtuais (VMs)
3. **Descrever** o que são imagens Docker e contêineres Docker
4. **Identificar** os benefícios de containerização para ML
5. **Avaliar** quando usar Docker em projetos de ciência de dados

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Aula 03 concluída (CI funcionando)
- Conta no Docker Hub (gratuita)
- Docker Desktop instalado

**Instalação do Docker Desktop:**

**Windows:**
1. Acesse https://www.docker.com/products/docker-desktop
2. Baixe o instalador para Windows
3. Execute e siga o wizard
4. Reinicie o computador
5. Abra Docker Desktop e aguarde inicialização

**Verificar instalação:**

```bash
# Verificar versão do Docker
docker --version

# Verificar que Docker está rodando
docker info

# Testar com container de exemplo
docker run hello-world
```

**Saída esperada do hello-world:**
```
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

**Checklist de Setup:**
- [ ] Docker Desktop instalado
- [ ] `docker --version` retorna versão
- [ ] `docker run hello-world` funciona
- [ ] Docker Desktop mostra status "Running"

# 5. Visão geral do que já existe no projeto (continuidade)

**Estado atual do projeto após Aula 03:**
```
swe4ds-credit-api/
├── .git/
├── .github/
│   └── workflows/
│       └── ci.yml               # CI com GitHub Actions
├── .dvc/
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

**O que faremos neste módulo (Aula 04):**
```
swe4ds-credit-api/
├── ...
├── Dockerfile                   # [NOVO] Definição da imagem
├── .dockerignore                # [NOVO] Arquivos a ignorar
├── docker-compose.yml           # [NOVO] Orquestração
└── ...
```

Nesta primeira parte, vamos entender a teoria. A partir da Parte 02, começamos a criar os arquivos.

# 6. Passo a passo (comandos + código)

## Passo 1: O Problema de Reprodutibilidade (Excalidraw: Slide 1)

**Intenção**: Entender profundamente o problema que Docker resolve.

### O que significa "funciona na minha máquina"?

Um projeto Python depende de múltiplas camadas:

```
┌─────────────────────────────────────────────────────────────────┐
│                    CAMADAS DE DEPENDÊNCIA                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Seu Código Python (data_loader.py, train.py, etc.)      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          │                                      │
│                          ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Bibliotecas Python (pandas, scikit-learn, numpy)        │   │
│  │ Versões específicas: pandas==2.2.3, sklearn==1.5.2      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          │                                      │
│                          ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Interpretador Python (3.12.0, 3.11.5, 3.10.8...)        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          │                                      │
│                          ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Bibliotecas do Sistema (libc, libssl, BLAS, LAPACK)     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          │                                      │
│                          ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Sistema Operacional (Windows 11, Ubuntu 22.04, macOS)   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

Quando qualquer camada muda, seu código pode quebrar!

### Cenários Reais de Quebra

| Cenário | Causa | Sintoma |
|---------|-------|---------|
| Versão de Python | Dev usa 3.12, prod tem 3.9 | SyntaxError em match/case |
| Versão de biblioteca | sklearn 1.5 vs 1.2 | Método não existe |
| Sistema operacional | Windows vs Linux | Paths quebrados (`\` vs `/`) |
| Bibliotecas do sistema | libblas diferente | Numpy dá resultados diferentes |
| Variáveis de ambiente | Falta PYTHONPATH | ModuleNotFoundError |

### Soluções Tradicionais (e suas limitações)

1. **requirements.txt** - Fixa versões Python, mas não o SO
2. **venv/virtualenv** - Isola Python, mas não bibliotecas do sistema
3. **Documentação** - Ninguém lê ou está sempre desatualizada
4. **Máquinas Virtuais** - Pesadas, lentas para iniciar

**CHECKPOINT**: Você consegue listar 3 formas pelas quais seu código pode quebrar em outra máquina?

---

## Passo 2: O que é Docker? (Excalidraw: Slide 1 - Contêiner)

**Intenção**: Entender os conceitos fundamentais.

### Definições Fundamentais

**Container (Contêiner)**: Um pacote executável que inclui:
- Código da aplicação
- Runtime (Python, Node, etc.)
- Bibliotecas e dependências
- Configurações

**Imagem Docker**: O "molde" ou "template" de um container. É um snapshot imutável de um sistema de arquivos + metadados.

**Analogia**:
- **Imagem** = Receita de bolo (instruções para criar)
- **Container** = Bolo pronto (instância executando)

### Imagem vs Container

```
┌─────────────────────────────────────────────────────────────────┐
│                    IMAGEM vs CONTAINER                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  IMAGEM (Template)                                              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  - Arquivo(s) no disco                                   │   │
│  │  - Imutável (read-only)                                  │   │
│  │  - Definida por um Dockerfile                            │   │
│  │  - Pode ser compartilhada (Docker Hub)                   │   │
│  │  - Múltiplos containers podem usar a mesma imagem        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          │                                      │
│                          │ docker run                           │
│                          ▼                                      │
│  CONTAINER (Instância)                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  - Processo em execução                                  │   │
│  │  - Tem estado (memória, CPU)                             │   │
│  │  - Isolado do host                                       │   │
│  │  - Pode ser parado, iniciado, deletado                   │   │
│  │  - Alterações são perdidas ao remover (exceto volumes)   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Demonstração Rápida

```bash
# Ver imagens locais
docker images

# Baixar uma imagem do Docker Hub
docker pull python:3.12-slim

# Ver imagens novamente
docker images

# Criar um container a partir da imagem
docker run -it python:3.12-slim python --version

# Listar containers (inclusive parados)
docker ps -a
```

**CHECKPOINT**: Você entende a diferença entre imagem e container?

---

## Passo 3: Containers vs Máquinas Virtuais (Excalidraw: Slide 2)

**Intenção**: Entender por que containers são mais eficientes que VMs.

### Arquitetura Comparada

```
┌─────────────────────────────────────────────────────────────────┐
│          MÁQUINA VIRTUAL              │        CONTAINER        │
├───────────────────────────────────────┼─────────────────────────┤
│                                       │                         │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ │ ┌─────┐ ┌─────┐ ┌─────┐│
│  │  App 1  │ │  App 2  │ │  App 3  │ │ │App 1│ │App 2│ │App 3││
│  ├─────────┤ ├─────────┤ ├─────────┤ │ ├─────┤ ├─────┤ ├─────┤│
│  │  Bins/  │ │  Bins/  │ │  Bins/  │ │ │Bins/│ │Bins/│ │Bins/││
│  │  Libs   │ │  Libs   │ │  Libs   │ │ │Libs │ │Libs │ │Libs ││
│  ├─────────┤ ├─────────┤ ├─────────┤ │ └──┬──┘ └──┬──┘ └──┬──┘│
│  │ Guest   │ │ Guest   │ │ Guest   │ │    │       │       │   │
│  │  OS     │ │  OS     │ │  OS     │ │    └───────┼───────┘   │
│  │ (Linux) │ │(Windows)│ │ (Linux) │ │            │           │
│  └────┬────┘ └────┬────┘ └────┬────┘ │   ┌────────┴────────┐  │
│       │           │           │      │   │  Docker Engine  │  │
│  ┌────┴───────────┴───────────┴────┐ │   └────────┬────────┘  │
│  │          HYPERVISOR             │ │            │           │
│  │   (VMware, VirtualBox, Hyper-V) │ │   ┌────────┴────────┐  │
│  └──────────────┬──────────────────┘ │   │    Host OS      │  │
│                 │                    │   │    (Linux)      │  │
│  ┌──────────────┴──────────────────┐ │   └────────┬────────┘  │
│  │           Host OS               │ │            │           │
│  └──────────────┬──────────────────┘ │   ┌────────┴────────┐  │
│                 │                    │   │   Hardware      │  │
│  ┌──────────────┴──────────────────┐ │   └─────────────────┘  │
│  │          Hardware               │ │                        │
│  └─────────────────────────────────┘ │                        │
│                                       │                        │
│  Cada VM tem SO completo             │ Containers compartilham│
│  GB de memória por VM                │ kernel do host         │
│  Minutos para iniciar                │ MB de memória          │
│                                       │ Segundos para iniciar  │
└───────────────────────────────────────┴─────────────────────────┘
```

### Comparação Detalhada

| Aspecto | Máquina Virtual | Container |
|---------|-----------------|-----------|
| **Isolamento** | SO completo | Processos isolados |
| **Tamanho** | GBs (inclui SO) | MBs (só app + deps) |
| **Inicialização** | Minutos | Segundos |
| **Overhead** | Alto (hypervisor) | Baixo (compartilha kernel) |
| **Portabilidade** | Limitada | Alta |
| **Densidade** | 10-20 por host | 100+ por host |
| **Segurança** | Isolamento forte | Isolamento moderado |

### Quando Usar Cada Um?

**Use VMs quando:**
- Precisa de sistemas operacionais diferentes (Linux + Windows)
- Requer isolamento de segurança forte
- Aplicações legadas que precisam de ambiente específico

**Use Containers quando:**
- Quer consistência entre dev e prod
- Precisa escalar rapidamente
- Quer portabilidade entre nuvens
- Microserviços e aplicações modernas

**Para Data Science**: Containers são a escolha padrão para deploy de modelos.

**CHECKPOINT**: Você consegue explicar por que containers são mais leves que VMs?

---

## Passo 4: Benefícios de Docker para Data Science (Excalidraw: Slide 2 - Benefícios)

**Intenção**: Entender valor específico para projetos de ML.

### 1. Reprodutibilidade Total

```
┌─────────────────────────────────────────────────────────────────┐
│                    REPRODUTIBILIDADE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ANTES (sem Docker):                                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ README.md:                                               │   │
│  │ "Para rodar: instale Python 3.12, rode pip install..."   │   │
│  │                                                          │   │
│  │ Realidade:                                               │   │
│  │ - Cada pessoa tem ambiente diferente                     │   │
│  │ - Instruções desatualizadas                              │   │
│  │ - Dependências implícitas do sistema                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  DEPOIS (com Docker):                                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ README.md:                                               │   │
│  │ "Para rodar: docker run minha-imagem"                    │   │
│  │                                                          │   │
│  │ Realidade:                                               │   │
│  │ - Todo mundo roda exatamente o mesmo ambiente            │   │
│  │ - Dockerfile É a documentação executável                 │   │
│  │ - Zero configuração manual                               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Colaboração Simplificada

- Novos membros produtivos em minutos (não dias)
- Não há "setup do ambiente" - só `docker run`
- Toda equipe usa ambiente idêntico

### 3. Deploy Simplificado

```
┌─────────────────────────────────────────────────────────────────┐
│                    PIPELINE DE DEPLOY                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Desenvolvimento         Testes           Produção              │
│  ┌───────────┐       ┌───────────┐     ┌───────────┐           │
│  │  Notebook │       │    CI     │     │  Servidor │           │
│  │   Local   │  ──►  │  GitHub   │ ──► │   AWS/GCP │           │
│  └───────────┘       │  Actions  │     └───────────┘           │
│       │              └───────────┘          │                   │
│       │                   │                 │                   │
│       └───────────────────┼─────────────────┘                   │
│                           │                                     │
│                   MESMA IMAGEM DOCKER                           │
│                                                                 │
│  Se funciona em dev, funciona em prod. Garantido.              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4. Versionamento de Ambiente

```bash
# Tag de versão específica
docker tag minha-api:latest minha-api:v1.2.3

# Rollback é trivial
docker run minha-api:v1.2.2  # Volta para versão anterior
```

### 5. Escalonamento

- Kubernetes orquestra containers
- De 1 para 100 instâncias facilmente
- Load balancing automático

**CHECKPOINT**: Liste 3 benefícios de Docker para seu projeto de ML.

---

## Passo 5: Arquitetura Docker (Conceitual)

**Intenção**: Entender os componentes do ecossistema Docker.

### Componentes Principais

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARQUITETURA DOCKER                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                     Docker Client                        │   │
│  │  (CLI: docker build, docker run, docker push)           │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │ REST API                            │
│                           ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Docker Daemon                         │   │
│  │  (dockerd - gerencia imagens, containers, networks)     │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│           ┌───────────────┼───────────────┐                    │
│           ▼               ▼               ▼                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Images    │  │ Containers  │  │  Networks   │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│           │                                                     │
│           │ docker pull/push                                   │
│           ▼                                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Docker Registry                       │   │
│  │  (Docker Hub, GitHub Container Registry, ECR, etc.)     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Fluxo de Trabalho Típico

```bash
# 1. Escrever Dockerfile (na próxima aula)
# 2. Construir imagem
docker build -t minha-api:v1 .

# 3. Testar localmente
docker run -p 8000:8000 minha-api:v1

# 4. Publicar no registry
docker push minha-api:v1

# 5. Em produção, baixar e rodar
docker pull minha-api:v1
docker run -d minha-api:v1
```

**CHECKPOINT**: Você entende o fluxo build → run → push → pull?

---

## Passo 6: Explorando Docker (Comandos Básicos)

**Intenção**: Familiarizar-se com a CLI do Docker.

### Comandos Essenciais

```bash
# Verificar versão
docker --version

# Informações do sistema
docker info

# Listar imagens locais
docker images

# Listar containers em execução
docker ps

# Listar todos os containers (inclusive parados)
docker ps -a

# Baixar imagem
docker pull python:3.12-slim

# Executar container interativo
docker run -it python:3.12-slim bash

# Dentro do container:
python --version
pip list
exit

# Remover container
docker rm <container_id>

# Remover imagem
docker rmi python:3.12-slim
```

### Exercício Guiado: Explorando uma Imagem Python

```bash
# Baixar imagem oficial Python
docker pull python:3.12-slim

# Verificar tamanho
docker images python:3.12-slim

# Executar e explorar
docker run -it python:3.12-slim bash

# Dentro do container:
cat /etc/os-release      # Ver sistema operacional
python --version         # Ver versão Python
pip list                 # Ver pacotes instalados
which python             # Onde está o Python
exit
```

**Saída esperada de `/etc/os-release`:**
```
PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
...
```

**CHECKPOINT**: Você conseguiu executar bash dentro de um container Python.

# 7. Testes rápidos e validação

**Verificar Docker funcionando:**

```bash
# Deve retornar versão
docker --version

# Deve mostrar informações do sistema
docker info | head -20

# Deve baixar e executar
docker run hello-world
```

**Verificar exploração de imagem:**

```bash
# Executar Python no container
docker run python:3.12-slim python -c "print('Hello from Docker!')"
```

**Esperado:**
```
Hello from Docker!
```

# 8. Observabilidade e boas práticas (mini-bloco)

### Boas Práticas Introdutórias

1. **Use imagens oficiais**
   - `python:3.12-slim` é oficial e mantida
   - Evite imagens de fontes desconhecidas
   - **Trade-off**: Menos customização, mais segurança

2. **Prefira imagens slim/alpine**
   - `python:3.12-slim` (~150MB) vs `python:3.12` (~900MB)
   - Menos superfície de ataque
   - **Trade-off**: Podem faltar algumas bibliotecas do sistema

3. **Versione suas tags**
   - Use `python:3.12-slim`, não `python:latest`
   - `latest` pode mudar e quebrar seu build
   - **Trade-off**: Precisa atualizar manualmente

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| `Cannot connect to Docker daemon` | Docker não está rodando | Inicie Docker Desktop |
| `Permission denied` (Linux) | Usuário não está no grupo docker | `sudo usermod -aG docker $USER` |
| `No space left on device` | Disco cheio de imagens/containers | `docker system prune -a` |
| `Image not found` | Nome/tag errado | Verifique em hub.docker.com |
| Lentidão no Windows | WSL2 não configurado | Habilite WSL2 nas configurações |
| `port already in use` | Porta ocupada | Use outra porta ou pare o processo |

# 10. Exercícios (básico e avançado)

## Exercício Básico 1: Explorar Imagem Data Science

Baixe e explore a imagem `jupyter/scipy-notebook`:

```bash
docker pull jupyter/scipy-notebook
docker run -it jupyter/scipy-notebook bash
# Dentro: verifique pandas, numpy, scipy instalados
```

**Critério de sucesso**: Listar versões de pandas, numpy e scipy dentro do container.

## Exercício Básico 2: Comparar Tamanhos

Compare o tamanho de diferentes imagens Python:

```bash
docker pull python:3.12
docker pull python:3.12-slim
docker pull python:3.12-alpine
docker images | grep python
```

**Critério de sucesso**: Documentar o tamanho de cada uma e explicar as diferenças.

## Exercício Avançado: Pesquisa sobre Base Images

Pesquise e documente:
1. Qual a diferença entre `slim`, `alpine` e a imagem padrão?
2. Por que `alpine` pode dar problemas com pandas/numpy?
3. Qual imagem base você escolheria para um projeto de ML e por quê?

**Critério de sucesso**: Documento de 1 página com justificativas técnicas.

# 11. Resultados e Lições

## Como Medir Sucesso

| Métrica | Como Medir | Esperado |
|---------|------------|----------|
| Docker instalado | `docker --version` | Versão retornada |
| Daemon rodando | `docker info` | Sem erros |
| Imagem baixada | `docker images` | python:3.12-slim listada |
| Container executado | `docker run hello-world` | Mensagem de sucesso |

## Lições Aprendidas

1. **"Funciona na minha máquina"** é um problema real e solucionável
2. **Containers** são mais leves que VMs - compartilham kernel
3. **Imagem** é o template, **container** é a instância em execução
4. **Docker** garante reprodutibilidade entre dev, teste e produção
5. **Imagens oficiais** e versionadas são melhores práticas

# 12. Encerramento e gancho para a próxima aula (script)

Excelente! Agora você entende por que Docker é tão importante para Data Science. Você sabe diferenciar containers de VMs, entende a relação entre imagens e containers, e conhece os benefícios de containerização para ML.

O Docker está instalado e funcionando. Você já explorou uma imagem Python por dentro.

Na próxima aula, vamos criar nosso primeiro **Dockerfile**. Vamos aprender a escrever as instruções para construir uma imagem personalizada para nossa API de crédito. Você vai entender cada linha do Dockerfile: FROM, COPY, RUN, CMD. E no final, terá uma imagem pronta para rodar sua aplicação.

Prepare-se para colocar a mão na massa! Até a próxima aula.
