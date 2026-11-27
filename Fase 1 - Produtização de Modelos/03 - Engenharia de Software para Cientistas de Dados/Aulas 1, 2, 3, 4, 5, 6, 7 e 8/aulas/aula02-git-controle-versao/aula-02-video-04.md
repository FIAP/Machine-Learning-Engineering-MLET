---
titulo: "Aula 02 – Parte 04: Versionando Dados e Modelos - Introdução Prática ao DVC"
modulo: "Engenharia de Software para Cientista de Dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 15
prerequisitos:
  - "Python 3.12+"
  - "UV instalado"
  - "Git configurado"
  - "Aula 02 - Partes 01, 02 e 03 concluídas"
  - "Repositório swe4ds-credit-api funcional"
tags: ["dvc", "data-version-control", "versionamento", "ml", "reprodutibilidade", "datasets"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula, vamos resolver um problema que todo cientista de dados enfrenta: como versionar não só o código, mas também os **dados** e os **modelos**?

O Git é fantástico para código, mas tem limitações com arquivos grandes. Imagine tentar versionar um dataset de 10GB ou um modelo de deep learning de 500MB. O Git simplesmente não foi feito para isso. E sem versionamento de dados, você perde reprodutibilidade.

Já imaginou precisar reproduzir um experimento de 6 meses atrás e não saber qual era a versão exata do dataset usado? Ou descobrir que o modelo que estava em produção foi treinado com dados diferentes do que você tem agora?

O **DVC (Data Version Control)** resolve exatamente isso. É como um Git para dados - integrado ao Git, mas projetado para arquivos grandes. Vamos implementá-lo no nosso projeto.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Seu modelo de ML está em produção e funciona bem. Três meses depois, você precisa re-treinar com dados atualizados. Você roda o script, mas os resultados são completamente diferentes. O que mudou? O código está igual. Ah... os dados mudaram! Mas você não tem a versão antiga.

**Agitação**: Você passa dias tentando recriar o dataset original. Backlogs de dados, transformações manuais, pipelines que mudaram. Você acha que reconstruiu, mas não tem certeza. O modelo retreinado tem métricas piores. Será problema do modelo ou dos dados? Impossível saber. Você está preso em um ciclo de incerteza. O cliente questiona a qualidade do seu trabalho.

**Solução**: Com DVC, cada versão do dataset fica vinculada ao commit do código. Você quer o dataset de 3 meses atrás? `git checkout v1.0 && dvc checkout`. Pronto. Os dados exatos daquele momento são restaurados. Você pode comparar modelos com confiança: mesmo código, mesmo dado = mesmo resultado. A reprodutibilidade está garantida.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Explicar** o problema de versionar dados grandes e por que Git não é suficiente
2. **Instalar e configurar** DVC em um projeto Git existente
3. **Rastrear** datasets e modelos com DVC
4. **Sincronizar** arquivos grandes com storages remotos (conceito)
5. **Alternar** entre versões de dados usando checkout
6. **Integrar** DVC no workflow de Data Science para garantir reprodutibilidade

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Git 2.40+ instalado e configurado
- Python 3.12+
- UV instalado
- Repositório `swe4ds-credit-api` funcional
- Conexão com internet (para baixar DVC)

**Instalação do DVC:**

```bash
# Navegar para o projeto
cd c:\Users\diogomiyake\projects\swe4ds-credit-api

# Ativar ambiente virtual
.venv\Scripts\activate

# Instalar DVC com UV
uv pip install dvc

# Verificar instalação
dvc version
```

**Saída esperada:**
```
DVC version: 3.x.x
Python version: 3.12.x
Platform: Windows-...
```

**Atualizar requirements:**
```bash
uv pip freeze > requirements.txt
git add requirements.txt
git commit -m "chore: adiciona DVC às dependências"
```

**Checklist de Setup:**
- [ ] DVC instalado e versão verificada
- [ ] Ambiente virtual ativo
- [ ] Repositório Git limpo (sem alterações pendentes)

# 5. Visão geral do que já existe no projeto (continuidade)

**Estrutura atual (após Aula 02 - Parte 03):**
```
swe4ds-credit-api/
├── .git/
├── .gitignore
├── .venv/
├── LICENSE
├── README.md
├── requirements.txt
├── util.txt
└── src/
    ├── __init__.py
    └── data_loader.py
```

**O que faremos nesta aula:**
```
swe4ds-credit-api/
├── .git/
├── .dvc/                  # [NOVO] Configurações do DVC
├── .dvcignore             # [NOVO] Arquivos ignorados pelo DVC
├── .gitignore             # [ATUALIZADO] Ignora arquivos grandes
├── LICENSE
├── README.md
├── requirements.txt
├── data/                  # [NOVO] Pasta de dados
│   ├── raw/               # [NOVO] Dados brutos
│   │   └── credit.csv.dvc # [NOVO] Pointer file
│   └── processed/         # [NOVO] Dados processados
├── models/                # [NOVO] Modelos treinados
│   └── .gitkeep
└── src/
    ├── __init__.py
    └── data_loader.py
```

# 6. Passo a passo (comandos + código)

## Passo 1: Entendendo o Problema (Excalidraw: Slide 10 - O que é DVC)

**Intenção**: Visualizar por que Git + DVC é melhor que Git sozinho.

### Git com Arquivos Grandes: Os Problemas

1. **Repositório inchado**: Cada versão do arquivo grande é armazenada
2. **Clone lento**: Baixar todo o histórico é demorado
3. **Limitações de hosting**: GitHub tem limite de 100MB por arquivo
4. **Diff impossível**: Git não consegue fazer diff de binários

### Como DVC Resolve

DVC usa uma estratégia inteligente:

```
┌─────────────────────────────────────────────────────────────────┐
│                    COMO DVC FUNCIONA                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Arquivo Original          Git                   Storage        │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐  │
│  │ credit.csv   │      │ credit.csv.  │      │ credit.csv   │  │
│  │ (500 MB)     │─────►│ dvc          │      │ (500 MB)     │  │
│  │              │      │ (300 bytes)  │─────►│ versionado   │  │
│  └──────────────┘      └──────────────┘      └──────────────┘  │
│                              │                                  │
│  O arquivo grande      Git versiona         S3/GCS/Local       │
│  NÃO vai pro Git       apenas o pointer     armazena o real    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

O Git versiona um arquivo `.dvc` pequeno (metadados). O arquivo real vai para um storage separado.

**CHECKPOINT**: Você entende que DVC separa o rastreamento do armazenamento?

---

## Passo 2: Inicializando DVC no Projeto

**Intenção**: Configurar DVC no repositório existente (Excalidraw: Slide 11 - Funcionalidades do DVC).

```bash
# Garantir que está na raiz do projeto
cd c:\Users\diogomiyake\projects\swe4ds-credit-api

# Inicializar DVC
dvc init
```

**Saída esperada:**
```
Initialized DVC repository.

You can now commit the changes to git.

+---------------------------------------------------------------------+
|                                                                     |
|        DVC has enabled anonymous aggregate usage analytics.         |
|     Read the analytics documentation (and hierarchical to opt-out): |
|             <https://dvc.org/doc/user-guide/analytics>              |
|                                                                     |
+---------------------------------------------------------------------+
```

**O que foi criado:**

```bash
# Ver arquivos criados
git status
```

```
Untracked files:
        .dvc/
        .dvcignore
```

### Estrutura .dvc/

```
.dvc/
├── config       # Configurações do DVC
├── .gitignore   # Ignora cache do DVC
└── cache/       # Cache local de dados
```

```bash
# Commitar inicialização
git add .dvc .dvcignore
git commit -m "chore: inicializa DVC para versionamento de dados"
```

**CHECKPOINT**: Pasta `.dvc/` existe e foi commitada.

---

## Passo 3: Criando Estrutura de Dados

**Intenção**: Organizar pastas para dados e modelos.

```bash
# Criar estrutura de pastas
mkdir -p data/raw data/processed models

# Criar .gitkeep para manter pastas vazias no Git
# Windows PowerShell:
New-Item -Path "data/raw/.gitkeep" -ItemType File
New-Item -Path "data/processed/.gitkeep" -ItemType File
New-Item -Path "models/.gitkeep" -ItemType File

# Linux/macOS:
# touch data/raw/.gitkeep data/processed/.gitkeep models/.gitkeep
```

### Atualizar .gitignore

Edite `.gitignore` para ignorar arquivos de dados grandes:

```bash
# Abrir .gitignore e adicionar ao final:
```

```gitignore
# Data files (managed by DVC)
/data/raw/*.csv
/data/raw/*.parquet
/data/raw/*.xlsx
/data/processed/*.csv
/data/processed/*.parquet

# Model artifacts (managed by DVC)
/models/*.pkl
/models/*.joblib
/models/*.h5
/models/*.pt
```

```bash
git add .gitignore data/
git commit -m "chore: estrutura de pastas para dados e modelos"
```

**CHECKPOINT**: Pastas `data/raw`, `data/processed` e `models` existem.

---

## Passo 4: Baixando e Rastreando um Dataset

**Intenção**: Adicionar um dataset real e versioná-lo com DVC.

### 4.1 Criar Script para Download

Crie `scripts/download_data.py`:

```bash
mkdir scripts
```

```python
# scripts/download_data.py
"""
Script para download do dataset de credit default.
"""
import urllib.request
import os
from pathlib import Path


def download_credit_dataset():
    """
    Baixa o dataset UCI Credit Card Default e salva localmente.
    
    Para fins didáticos, vamos criar um dataset de exemplo.
    Em produção, você baixaria de uma fonte real.
    """
    output_dir = Path("data/raw")
    output_file = output_dir / "credit_sample.csv"
    
    # Criar diretório se não existir
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Para a aula, vamos criar um dataset de exemplo
    # Em produção, você baixaria o dataset real
    print("Criando dataset de exemplo...")
    
    import random
    
    # Gerar dados de exemplo
    header = "ID,LIMIT_BAL,SEX,EDUCATION,MARRIAGE,AGE,PAY_0,PAY_2,PAY_3,PAY_4,PAY_5,PAY_6,BILL_AMT1,BILL_AMT2,BILL_AMT3,BILL_AMT4,BILL_AMT5,BILL_AMT6,PAY_AMT1,PAY_AMT2,PAY_AMT3,PAY_AMT4,PAY_AMT5,PAY_AMT6,default\n"
    
    rows = []
    for i in range(1, 1001):  # 1000 registros de exemplo
        row = [
            i,                              # ID
            random.randint(10000, 500000),  # LIMIT_BAL
            random.randint(1, 2),           # SEX
            random.randint(1, 4),           # EDUCATION
            random.randint(1, 3),           # MARRIAGE
            random.randint(21, 70),         # AGE
            random.randint(-2, 8),          # PAY_0
            random.randint(-2, 8),          # PAY_2
            random.randint(-2, 8),          # PAY_3
            random.randint(-2, 8),          # PAY_4
            random.randint(-2, 8),          # PAY_5
            random.randint(-2, 8),          # PAY_6
            random.randint(0, 100000),      # BILL_AMT1
            random.randint(0, 100000),      # BILL_AMT2
            random.randint(0, 100000),      # BILL_AMT3
            random.randint(0, 100000),      # BILL_AMT4
            random.randint(0, 100000),      # BILL_AMT5
            random.randint(0, 100000),      # BILL_AMT6
            random.randint(0, 50000),       # PAY_AMT1
            random.randint(0, 50000),       # PAY_AMT2
            random.randint(0, 50000),       # PAY_AMT3
            random.randint(0, 50000),       # PAY_AMT4
            random.randint(0, 50000),       # PAY_AMT5
            random.randint(0, 50000),       # PAY_AMT6
            random.randint(0, 1),           # default
        ]
        rows.append(",".join(map(str, row)) + "\n")
    
    # Escrever arquivo
    with open(output_file, "w") as f:
        f.write(header)
        f.writelines(rows)
    
    print(f"Dataset salvo em: {output_file}")
    print(f"Tamanho: {output_file.stat().st_size / 1024:.2f} KB")
    print(f"Registros: {len(rows)}")
    
    return output_file


if __name__ == "__main__":
    download_credit_dataset()
```

### 4.2 Executar o Download

```bash
python scripts/download_data.py
```

**Saída esperada:**
```
Criando dataset de exemplo...
Dataset salvo em: data/raw/credit_sample.csv
Tamanho: XX.XX KB
Registros: 1000
```

### 4.3 Adicionar ao DVC (NÃO ao Git!)

```bash
# Rastrear arquivo com DVC
dvc add data/raw/credit_sample.csv
```

**Saída esperada:**
```
To track the changes with git, run:

    git add data/raw/credit_sample.csv.dvc data/raw/.gitignore
```

**O que aconteceu:**
- DVC criou `credit_sample.csv.dvc` (pointer file)
- DVC atualizou `data/raw/.gitignore` para ignorar o arquivo real
- O arquivo real foi movido para o cache do DVC

### 4.4 Verificar o Pointer File

```bash
cat data/raw/credit_sample.csv.dvc
```

**Saída:**
```yaml
outs:
- md5: a1b2c3d4e5f6...  # Hash único do arquivo
  size: 123456          # Tamanho em bytes
  path: credit_sample.csv
```

Este pequeno arquivo é o que o Git vai versionar!

### 4.5 Commitar no Git

```bash
# Adicionar script e pointer file
git add scripts/download_data.py data/raw/credit_sample.csv.dvc data/raw/.gitignore
git commit -m "feat: adiciona dataset de credit com DVC

- Script de download em scripts/download_data.py
- Dataset rastreado via DVC (1000 registros de exemplo)"
```

**CHECKPOINT**: O arquivo `.dvc` existe e foi commitado, mas o `.csv` não.

---

## Passo 5: Atualizando Dados e Criando Nova Versão

**Intenção**: Mostrar como versionar mudanças nos dados (Excalidraw: Slide 12 - Reprodutibilidade Completa).

### 5.1 Modificar o Dataset

Edite `scripts/download_data.py` para gerar 2000 registros:

```python
# Altere a linha:
for i in range(1, 1001):  # 1000 registros de exemplo

# Para:
for i in range(1, 2001):  # 2000 registros de exemplo
```

### 5.2 Regenerar o Dataset

```bash
python scripts/download_data.py
```

**Saída:**
```
Criando dataset de exemplo...
Dataset salvo em: data/raw/credit_sample.csv
Tamanho: XX.XX KB
Registros: 2000
```

### 5.3 Atualizar Rastreamento DVC

```bash
# DVC detecta que o arquivo mudou
dvc status
```

**Saída:**
```
data/raw/credit_sample.csv.dvc:
    changed outs:
        modified:           data/raw/credit_sample.csv
```

```bash
# Atualizar o rastreamento
dvc add data/raw/credit_sample.csv

# Commitar nova versão
git add data/raw/credit_sample.csv.dvc scripts/download_data.py
git commit -m "feat: expande dataset para 2000 registros"
```

**CHECKPOINT**: Novo commit com o `.dvc` atualizado.

---

## Passo 6: Alternando Entre Versões

**Intenção**: Demonstrar a reprodutibilidade - voltar para versão anterior dos dados.

```bash
# Ver histórico de commits
git log --oneline -5

# Voltar para versão anterior (1000 registros)
git checkout HEAD~1 -- data/raw/credit_sample.csv.dvc

# Restaurar o arquivo real correspondente
dvc checkout data/raw/credit_sample.csv.dvc

# Verificar tamanho (deve ser menor)
ls -la data/raw/credit_sample.csv
```

O arquivo agora tem a versão anterior!

```bash
# Voltar para a versão atual
git checkout HEAD -- data/raw/credit_sample.csv.dvc
dvc checkout data/raw/credit_sample.csv.dvc
```

**CHECKPOINT**: Você conseguiu alternar entre versões do dataset.

---

## Passo 7: Conceito de Remote Storage (Visão Geral)

**Intenção**: Explicar como compartilhar dados grandes com a equipe.

### Storage Remoto

Por padrão, DVC armazena no cache local. Para colaboração, configure um remote:

```bash
# Exemplo: configurar pasta local como "remote" (para teste)
mkdir -p ../dvc-storage
dvc remote add -d myremote ../dvc-storage

# Em produção, você usaria:
# dvc remote add -d s3remote s3://meu-bucket/dvc-cache
# dvc remote add -d gcsremote gs://meu-bucket/dvc-cache
```

### Push e Pull de Dados

```bash
# Enviar dados para remote
dvc push

# Baixar dados do remote (em outra máquina)
dvc pull
```

Este fluxo é análogo a `git push` e `git pull`, mas para dados!

### Fluxo Completo de Reprodutibilidade

```
┌─────────────────────────────────────────────────────────────────┐
│              FLUXO DE REPRODUTIBILIDADE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Desenvolvedor A                    Desenvolvedor B             │
│  ┌──────────────┐                  ┌──────────────┐            │
│  │ git commit   │                  │ git clone    │            │
│  │ dvc push     │────────────────► │ git checkout │            │
│  │              │                  │ dvc pull     │            │
│  └──────────────┘                  └──────────────┘            │
│         │                                 │                     │
│         ▼                                 ▼                     │
│  ┌──────────────┐                  ┌──────────────┐            │
│  │ GitHub:      │                  │ Mesmo código │            │
│  │ .dvc files   │                  │ Mesmos dados │            │
│  │              │                  │ = Reprodução!│            │
│  └──────────────┘                  └──────────────┘            │
│                                                                 │
│  ┌──────────────────────────────────────────────────┐          │
│  │              Storage (S3/GCS/Local)              │          │
│  │              Dados reais versionados             │          │
│  └──────────────────────────────────────────────────┘          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**CHECKPOINT**: Você entende o fluxo push/pull do DVC?

---

## Passo 8: Finalizando e Limpando

**Intenção**: Deixar o repositório organizado.

```bash
# Ver status final
git status
dvc status

# Push final para GitHub
git push origin main

# Ver estrutura final
tree . /F
```

**Estrutura final:**
```
swe4ds-credit-api/
├── .dvc/
│   ├── config
│   ├── .gitignore
│   └── cache/
├── .dvcignore
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   │   ├── .gitignore
│   │   ├── .gitkeep
│   │   └── credit_sample.csv.dvc
│   └── processed/
│       └── .gitkeep
├── models/
│   └── .gitkeep
├── scripts/
│   └── download_data.py
├── src/
│   ├── __init__.py
│   └── data_loader.py
└── util.txt
```

# 7. Testes rápidos e validação

**Verificar DVC está funcionando:**
```bash
dvc version
dvc status
```

Esperado: Versão do DVC e "Data and calculation are up to date."

**Verificar arquivo está rastreado:**
```bash
ls data/raw/*.dvc
```

Esperado: `credit_sample.csv.dvc`

**Verificar Git ignora o CSV:**
```bash
git status
```

Esperado: Nenhum arquivo `.csv` pendente.

**Teste de integridade:**
```bash
dvc diff HEAD~1
```

Esperado: Mostra diferenças entre versões do dataset.

# 8. Observabilidade e boas práticas (mini-bloco)

### Boas Práticas Aplicadas

1. **Separar dados brutos de processados**
   - `data/raw/` para dados originais
   - `data/processed/` para dados transformados
   - **Trade-off**: Mais organização, mais espaço de armazenamento

2. **Versionar scripts de download junto com dados**
   - Script que gera o dado fica no mesmo commit que o `.dvc`
   - Garante reprodutibilidade completa
   - **Trade-off**: Nenhum - é puramente vantajoso

3. **Usar remote storage para colaboração**
   - Dados compartilhados entre equipe
   - Backup automático
   - **Trade-off**: Custo de storage (S3, GCS)

4. **Commits atômicos incluem código E dados**
   - Mudou preprocessamento? Commit com código + novo `.dvc`
   - **Trade-off**: Disciplina maior, rastreabilidade perfeita

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| `ERROR: failed to pull data` | Arquivo não está no cache | Execute `dvc add` novamente |
| `ERROR: output 'X' is already tracked by SCM` | Arquivo está no Git e no DVC | Remove do Git com `git rm --cached` |
| `WARNING: Cache 'X' not found` | Cache foi apagado | Use `dvc pull` de um remote |
| `DVC not initialized` | Fora da pasta do projeto | Use `cd` para entrar no projeto |
| `Corrupted cache` | Hash não confere | Delete cache e `dvc checkout` |
| `.dvc file outdated` | Arquivo mudou sem `dvc add` | Execute `dvc add arquivo` |

# 10. Exercícios (básico e avançado)

## Exercício Básico 1: Rastrear Outro Arquivo

1. Crie um arquivo `data/raw/config.json` com configurações
2. Rastreie com `dvc add`
3. Faça commit do `.dvc` file

**Critério de sucesso**: `config.json.dvc` existe e está commitado.

## Exercício Básico 2: Alternar Versões

1. Modifique o `credit_sample.csv` (mude número de registros)
2. `dvc add` e commit
3. Use `git checkout` + `dvc checkout` para voltar à versão anterior
4. Verifique que o arquivo voltou ao estado anterior

**Critério de sucesso**: Arquivo restaurado com tamanho/conteúdo da versão anterior.

## Exercício Avançado: Simular Colaboração

1. Configure um remote local: `dvc remote add -d localremote ../dvc-storage`
2. Execute `dvc push`
3. Delete o cache local: `rm -rf .dvc/cache`
4. Execute `dvc pull`
5. Verifique que os dados foram restaurados

**Critério de sucesso**: Dados recuperados do remote sem o cache local.

# 11. Resultados e Lições

## Como Medir o Sucesso

| Métrica | Como Medir | Valor Esperado |
|---------|------------|----------------|
| DVC inicializado | Pasta `.dvc/` existe | Sim |
| Dataset rastreado | `dvc status` sem pendências | "Data and pipelines are up to date" |
| Git limpo | Nenhum arquivo grande no Git | `.csv` não listado em `git status` |
| Histórico funcional | `dvc diff HEAD~1` mostra mudanças | Lista diferenças de dados |

## Lições Aprendidas

1. **Git + DVC = Reprodutibilidade completa** - código E dados versionados juntos
2. **Pointer files são leves** - Git versiona metadados, não dados
3. **Cache local acelera o dia a dia** - dados ficam disponíveis localmente
4. **Remote storage habilita colaboração** - equipe compartilha dados grandes
5. **Disciplina de versionar dados vale a pena** - evita dores de cabeça futuras

# 12. Encerramento e gancho para a próxima aula (script)

Parabéns! Você completou a jornada de Git e controle de versão! Nesta aula, aprendemos a estender o poder do Git para dados e modelos usando DVC. Agora você tem as ferramentas para garantir reprodutibilidade completa nos seus projetos de Data Science.

Vamos recapitular o que construímos na Aula 02:
- Entendemos Git como sistema distribuído
- Criamos repositório, fizemos commits, branches e Pull Requests
- Resolvemos conflitos de merge e usamos comandos avançados
- Integramos DVC para versionar datasets

Na próxima aula, vamos mudar o foco para **testes automatizados**. Você vai aprender sobre a pirâmide de testes, escrever testes unitários com Pytest, e implementar TDD (Test-Driven Development) no contexto de Data Science.

Pense nisso: agora que sabemos versionar código e dados, como garantir que o código realmente funciona como esperado? Testes são a resposta. E vamos aplicá-los diretamente no nosso projeto de API de crédito.

Até a próxima aula!
