---
titulo: "Aula 03 – Parte 04: CI/CD Pipeline - Automatizando Testes com GitHub Actions"
modulo: "Engenharia de Software para Cientista de Dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 15
prerequisitos:
  - "Python 3.12+"
  - "UV instalado"
  - "Aula 03 - Partes 01 a 03 concluídas"
  - "Conta GitHub"
  - "Repositório swe4ds-credit-api com testes funcionando"
tags: ["github-actions", "ci-cd", "pipeline", "automacao", "tdd"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Essa é a última aula do módulo de testes automatizados, e vamos fechar com chave de ouro. Até agora, você escreveu testes e roda manualmente com `pytest`. Funciona, mas depende de você lembrar de rodar.

Nesta aula, vamos configurar **GitHub Actions** para rodar os testes automaticamente a cada push. Isso é **Integração Contínua (CI)** - um dos pilares do DevOps moderno. Código quebrado não entra mais no repositório sem que você saiba.

Vamos também fazer um exercício rápido de **TDD completo**, para você ver o ciclo Red → Green → Refactor funcionando na prática. Em 15 minutos, você terá um pipeline profissional de CI configurado.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Seu projeto tem testes. Você roda localmente, tudo passa. Você faz push. Seu colega faz pull, modifica algo, faz push. Os testes dele quebraram, mas ele esqueceu de rodar pytest. Agora o código no main está quebrado e ninguém sabe.

**Agitação**: Você descobre o problema dias depois, quando tenta fazer deploy. O bug foi introduzido há 15 commits. Quem quebrou? O quê quebrou? Você gasta horas fazendo git bisect para encontrar o commit culpado. Produtividade despencou.

**Solução**: GitHub Actions roda testes em cada push automaticamente. Se falhar, o commit é marcado com ❌ vermelho. Pull requests só podem ser mergeados se os testes passarem. Problemas são detectados em minutos, não dias. Cada commit tem um status claro: ✅ ou ❌.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Configurar** GitHub Actions para rodar testes automaticamente
2. **Criar** workflow YAML para CI de projeto Python
3. **Interpretar** resultados de execução no GitHub
4. **Aplicar** o ciclo TDD completo (Red → Green → Refactor)
5. **Configurar** branch protection para exigir testes passando

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Repositório `swe4ds-credit-api` no GitHub
- Testes funcionando localmente (`pytest` passa)
- Conta GitHub com permissões de escrita

**Verificar estado atual:**

```bash
cd c:\Users\diogomiyake\projects\swe4ds-credit-api
.venv\Scripts\activate

# Verificar testes passam
pytest tests/unit/ -v

# Verificar repositório está em dia
git status
git remote -v
```

**Checklist:**
- [ ] Testes passando localmente
- [ ] Repositório conectado ao GitHub
- [ ] Sem alterações não commitadas

# 5. Visão geral do que já existe no projeto (continuidade)

**Estado atual:**
```
swe4ds-credit-api/
├── .git/
├── .dvc/
├── .gitignore
├── .venv/
├── pyproject.toml
├── requirements.txt
├── src/
│   ├── __init__.py
│   └── data_loader.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── unit/
        ├── __init__.py
        └── test_data_loader.py
```

**O que vamos adicionar:**
```
swe4ds-credit-api/
├── .github/                   # [NOVO]
│   └── workflows/             # [NOVO]
│       └── ci.yml             # [NOVO] Pipeline de CI
├── src/
│   └── validation.py          # [NOVO] Criado com TDD
└── tests/
    └── unit/
        └── test_validation.py # [NOVO] Testes TDD
```

# 6. Passo a passo (comandos + código)

## Passo 1: Entendendo GitHub Actions (Excalidraw: Slide 7)

**Intenção**: Conhecer a ferramenta antes de usar.

### O que é GitHub Actions?

**GitHub Actions** é uma plataforma de CI/CD integrada ao GitHub que:
- Executa workflows automaticamente em eventos (push, PR, schedule)
- Roda em máquinas virtuais gerenciadas pelo GitHub
- Suporta Linux, Windows, macOS
- É gratuito para repositórios públicos

### Conceitos-Chave

```
┌─────────────────────────────────────────────────────────────────┐
│                    GITHUB ACTIONS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  WORKFLOW (.github/workflows/*.yml)                            │
│  └─ Arquivo YAML que define automação                          │
│                                                                 │
│  TRIGGER (on: push, pull_request)                              │
│  └─ Evento que inicia o workflow                               │
│                                                                 │
│  JOB (jobs: test:)                                             │
│  └─ Conjunto de steps que rodam na mesma máquina               │
│                                                                 │
│  STEP (- name: Run tests)                                      │
│  └─ Comando ou action individual                               │
│                                                                 │
│  RUNNER (runs-on: ubuntu-latest)                               │
│  └─ Máquina virtual onde job executa                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**CHECKPOINT**: Você entende a hierarquia Workflow → Job → Step?

---

## Passo 2: Criando Workflow de CI

**Intenção**: Configurar pipeline que roda testes automaticamente.

### Criar Estrutura de Diretórios

```bash
# Criar pasta de workflows
mkdir -p .github/workflows
```

### Criar Arquivo de Workflow

Crie `.github/workflows/ci.yml`:

```yaml
# .github/workflows/ci.yml
# Pipeline de Integração Contínua para swe4ds-credit-api
#
# Este workflow é acionado em:
# - Push para branch main
# - Pull requests para branch main
#
# Executa:
# - Linting com ruff (opcional)
# - Testes com pytest
# - Cobertura de código

name: CI

# Quando executar
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

# Variáveis de ambiente
env:
  PYTHON_VERSION: "3.12"

jobs:
  test:
    name: Testes Unitários
    runs-on: ubuntu-latest
    
    steps:
      # 1. Checkout do código
      - name: Checkout do repositório
        uses: actions/checkout@v4
      
      # 2. Setup Python
      - name: Configurar Python ${{ env.PYTHON_VERSION }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      # 3. Instalar UV (gerenciador de pacotes rápido)
      - name: Instalar UV
        run: |
          curl -LsSf https://astral.sh/uv/install.sh | sh
          echo "$HOME/.cargo/bin" >> $GITHUB_PATH
      
      # 4. Instalar dependências
      - name: Instalar dependências
        run: |
          uv pip install --system -r requirements.txt
          uv pip install --system pytest pytest-cov
      
      # 5. Rodar testes com cobertura
      - name: Executar testes
        run: |
          pytest tests/ -v --cov=src --cov-report=xml --cov-report=term-missing
      
      # 6. Upload do relatório de cobertura (opcional)
      - name: Upload cobertura para Codecov
        uses: codecov/codecov-action@v4
        if: always()
        with:
          file: ./coverage.xml
          fail_ci_if_error: false
          verbose: true
        env:
          CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
```

**Explicação de cada step:**

| Step | Propósito |
|------|-----------|
| Checkout | Baixa código do repositório |
| Setup Python | Instala Python na versão especificada |
| Instalar UV | Instala gerenciador de pacotes UV |
| Instalar deps | Instala requirements + pytest |
| Executar testes | Roda pytest com cobertura |
| Upload cobertura | Envia relatório para Codecov |

**CHECKPOINT**: Arquivo `ci.yml` criado.

---

## Passo 3: Configuração Simplificada (Alternativa sem UV)

**Intenção**: Oferecer versão mais simples para quem preferir.

Se preferir usar pip padrão:

```yaml
# .github/workflows/ci-simple.yml
name: CI (Simple)

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"  # Cache de dependências
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: pytest tests/ -v --cov=src
```

Escolha uma das versões, não as duas.

**CHECKPOINT**: Você tem uma versão do workflow CI pronta.

---

## Passo 4: Fazendo Push e Verificando Execução

**Intenção**: Ver o pipeline rodando no GitHub.

```bash
# Adicionar workflow
git add .github/workflows/ci.yml

# Commit
git commit -m "ci: adiciona workflow de testes automatizados

- Configura GitHub Actions para CI
- Roda pytest em cada push e PR
- Gera relatório de cobertura"

# Push para GitHub
git push origin main
```

### Verificar Execução no GitHub

1. Acesse seu repositório no GitHub
2. Clique na aba **Actions**
3. Você verá o workflow "CI" em execução
4. Clique para ver detalhes de cada step

```
┌─────────────────────────────────────────────────────────────────┐
│  GitHub Actions                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  CI                                                             │
│  ├─ ✅ Checkout do repositório (1s)                            │
│  ├─ ✅ Configurar Python 3.12 (5s)                             │
│  ├─ ✅ Instalar UV (3s)                                        │
│  ├─ ✅ Instalar dependências (8s)                              │
│  ├─ ✅ Executar testes (4s)                                    │
│  │   └─ 21 passed                                              │
│  └─ ✅ Upload cobertura (2s)                                   │
│                                                                 │
│  Status: ✅ Success                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**CHECKPOINT**: Workflow executou com sucesso no GitHub.

---

## Passo 5: Exercício TDD Completo (Excalidraw: Slide 8)

**Intenção**: Praticar o ciclo Red → Green → Refactor com código real.

Vamos criar uma função de validação usando TDD.

### RED - Escrever Teste que Falha

Crie `tests/unit/test_validation.py`:

```python
# tests/unit/test_validation.py
"""
Testes para módulo de validação.

Criados usando TDD - testes escritos ANTES da implementação.
"""
import pytest


class TestValidateLimitBal:
    """Testes para validação de limite de crédito."""
    
    def test_rejects_negative_limit(self):
        """Limite negativo deve ser rejeitado."""
        from src.validation import validate_limit_bal
        
        assert validate_limit_bal(-1000) is False
    
    def test_rejects_zero_limit(self):
        """Limite zero deve ser rejeitado."""
        from src.validation import validate_limit_bal
        
        assert validate_limit_bal(0) is False
    
    def test_accepts_valid_limit(self):
        """Limite válido (positivo) deve ser aceito."""
        from src.validation import validate_limit_bal
        
        assert validate_limit_bal(50000) is True
    
    def test_rejects_excessive_limit(self):
        """Limite muito alto (> 1 milhão) deve ser rejeitado."""
        from src.validation import validate_limit_bal
        
        assert validate_limit_bal(2_000_000) is False
    
    @pytest.mark.parametrize("value,expected", [
        (1, True),           # Mínimo válido
        (500_000, True),     # Médio
        (1_000_000, True),   # Máximo válido
        (1_000_001, False),  # Acima do máximo
    ])
    def test_boundary_cases(self, value, expected):
        """Testa valores nos limites."""
        from src.validation import validate_limit_bal
        
        assert validate_limit_bal(value) is expected
```

**Rodar testes (devem FALHAR):**

```bash
pytest tests/unit/test_validation.py -v
```

**Saída esperada:**
```
ModuleNotFoundError: No module named 'src.validation'
```

✅ **RED** alcançado! Testes falham porque o módulo não existe.

---

### GREEN - Código Mínimo para Passar

Crie `src/validation.py`:

```python
# src/validation.py
"""
Módulo de validação para dados de crédito.

Criado usando TDD - implementação guiada por testes.
"""


def validate_limit_bal(value: int | float) -> bool:
    """
    Valida se o limite de crédito é aceitável.
    
    Args:
        value: Valor do limite de crédito.
        
    Returns:
        True se válido, False caso contrário.
        
    Examples:
        >>> validate_limit_bal(50000)
        True
        >>> validate_limit_bal(-1000)
        False
        >>> validate_limit_bal(2_000_000)
        False
    """
    MIN_LIMIT = 1
    MAX_LIMIT = 1_000_000
    
    return MIN_LIMIT <= value <= MAX_LIMIT
```

**Rodar testes:**

```bash
pytest tests/unit/test_validation.py -v
```

**Saída esperada:**
```
tests/unit/test_validation.py::TestValidateLimitBal::test_rejects_negative_limit PASSED
tests/unit/test_validation.py::TestValidateLimitBal::test_rejects_zero_limit PASSED
tests/unit/test_validation.py::TestValidateLimitBal::test_accepts_valid_limit PASSED
tests/unit/test_validation.py::TestValidateLimitBal::test_rejects_excessive_limit PASSED
tests/unit/test_validation.py::TestValidateLimitBal::test_boundary_cases[1-True] PASSED
tests/unit/test_validation.py::TestValidateLimitBal::test_boundary_cases[500000-True] PASSED
tests/unit/test_validation.py::TestValidateLimitBal::test_boundary_cases[1000000-True] PASSED
tests/unit/test_validation.py::TestValidateLimitBal::test_boundary_cases[1000001-False] PASSED
```

✅ **GREEN** alcançado! Todos os testes passam.

---

### REFACTOR - Melhorar o Código

Agora podemos melhorar sem medo, pois testes protegem:

```python
# src/validation.py
"""
Módulo de validação para dados de crédito.

Funções de validação para garantir qualidade dos dados
antes de processamento e predição.
"""
from typing import TypeAlias

# Type alias para valores numéricos
NumericValue: TypeAlias = int | float

# Constantes de validação
LIMIT_BAL_MIN: int = 1
LIMIT_BAL_MAX: int = 1_000_000

AGE_MIN: int = 18
AGE_MAX: int = 100

VALID_EDUCATION: tuple[int, ...] = (1, 2, 3, 4)
VALID_MARRIAGE: tuple[int, ...] = (1, 2, 3)


def validate_limit_bal(value: NumericValue) -> bool:
    """
    Valida se o limite de crédito é aceitável.
    
    Limite deve estar entre 1 e 1.000.000.
    
    Args:
        value: Valor do limite de crédito.
        
    Returns:
        True se válido (1 <= value <= 1.000.000), False caso contrário.
    """
    return LIMIT_BAL_MIN <= value <= LIMIT_BAL_MAX


def validate_age(value: NumericValue) -> bool:
    """
    Valida se a idade é aceitável para análise de crédito.
    
    Idade deve estar entre 18 e 100 anos.
    
    Args:
        value: Idade em anos.
        
    Returns:
        True se válido (18 <= value <= 100), False caso contrário.
    """
    return AGE_MIN <= value <= AGE_MAX


def validate_education(value: int) -> bool:
    """
    Valida código de educação.
    
    Códigos válidos:
    - 1: Graduate school
    - 2: University
    - 3: High school
    - 4: Others
    
    Args:
        value: Código de educação.
        
    Returns:
        True se válido, False caso contrário.
    """
    return value in VALID_EDUCATION


def validate_marriage(value: int) -> bool:
    """
    Valida código de estado civil.
    
    Códigos válidos:
    - 1: Married
    - 2: Single
    - 3: Others
    
    Args:
        value: Código de estado civil.
        
    Returns:
        True se válido, False caso contrário.
    """
    return value in VALID_MARRIAGE
```

**Rodar testes após refactor:**

```bash
pytest tests/unit/test_validation.py -v
```

✅ **REFACTOR** completo! Testes continuam passando.

**CHECKPOINT**: Ciclo TDD completo - Red → Green → Refactor.

---

## Passo 6: Commit e Ver Pipeline Rodando com Novos Testes

**Intenção**: Verificar que CI detecta novos testes.

```bash
# Adicionar arquivos
git add src/validation.py tests/unit/test_validation.py

# Commit
git commit -m "feat: adiciona módulo de validação com TDD

Funções implementadas:
- validate_limit_bal: Valida limite de crédito
- validate_age: Valida idade
- validate_education: Valida código de educação
- validate_marriage: Valida código de estado civil

Testes: 8 novos testes unitários"

# Push
git push origin main
```

Acesse GitHub → Actions para ver o pipeline rodando com os novos testes.

**CHECKPOINT**: Pipeline passa com 29+ testes.

---

## Passo 7: Branch Protection (Opcional)

**Intenção**: Configurar proteção para exigir testes passando antes de merge.

### No GitHub:

1. Vá em **Settings** → **Branches**
2. Clique **Add rule** ou **Add branch protection rule**
3. Em "Branch name pattern": `main`
4. Marque:
   - ✅ **Require a pull request before merging**
   - ✅ **Require status checks to pass before merging**
   - Selecione: `test`
5. Clique **Create** ou **Save changes**

Agora, PRs só podem ser mergeados se o workflow `test` passar!

```
┌─────────────────────────────────────────────────────────────────┐
│  Pull Request: feat/nova-feature                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ❌ Some checks were not successful                             │
│     └─ ❌ test — 3 failed                                       │
│                                                                 │
│  [Merge pull request] ← Botão DESABILITADO                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**CHECKPOINT**: Branch protection configurada.

# 7. Testes rápidos e validação

```bash
# Verificar testes locais
pytest tests/ -v

# Verificar cobertura
pytest --cov=src --cov-report=term-missing

# Verificar workflow existe
cat .github/workflows/ci.yml
```

**Esperado:**
- Todos os testes passando
- Cobertura > 80%
- Arquivo ci.yml existe

# 8. Observabilidade e boas práticas (mini-bloco)

### Boas Práticas de CI

1. **Testes rápidos no CI**
   - CI deve completar em < 5 minutos
   - Testes lentos marcados com `@pytest.mark.slow`
   - **Trade-off**: Pode pular testes importantes

2. **Cache de dependências**
   - Use `cache: "pip"` no setup-python
   - Acelera execuções subsequentes
   - **Trade-off**: Cache pode ficar stale

3. **Fail fast**
   - Configure `fail-fast: true` em matrix
   - Para no primeiro erro
   - **Trade-off**: Menos feedback paralelo

4. **Relatórios de cobertura**
   - Upload para Codecov ou similar
   - Visualize tendências
   - **Trade-off**: Mais um serviço para configurar

5. **Branch protection**
   - Exija testes passando para merge
   - Protege branch main
   - **Trade-off**: Pode bloquear merges urgentes

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| Workflow não aparece | Arquivo no lugar errado | Deve estar em `.github/workflows/` |
| Erro de sintaxe YAML | Indentação incorreta | Use 2 espaços, não tabs |
| `ModuleNotFoundError` | Pythonpath incorreto | Adicione `PYTHONPATH: .` em env |
| Testes passam local, falham CI | Dependência faltando | Adicione ao requirements.txt |
| UV não encontrado | PATH incorreto | Adicione ao GITHUB_PATH |
| Workflow não dispara | Trigger errado | Verifique `on:` no YAML |

# 10. Exercícios (básico e avançado)

## Exercício Básico 1: Adicionar Step de Linting

Adicione um step para rodar `ruff` antes dos testes:

```yaml
- name: Lint com Ruff
  run: |
    uv pip install --system ruff
    ruff check src/ tests/
```

**Critério**: Workflow passa com linting.

## Exercício Básico 2: TDD para validate_age

Complete o ciclo TDD para `validate_age`:

1. Escreva 5 testes em `test_validation.py`
2. Verifique que falham (função ainda não testada nos testes)
3. Implemente (já está no código refatorado)
4. Verifique que passam

**Critério**: 5 novos testes passando.

## Exercício Avançado: Matrix de Versões Python

Configure o workflow para testar em múltiplas versões do Python:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]
    
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      # ... resto dos steps
```

**Critério**: Workflow roda em 3 versões de Python.

# 11. Resultados e Lições

## Métricas Finais do Módulo

| Métrica | Aula 01 | Aula 02 | Aula 03 | Aula 04 |
|---------|---------|---------|---------|---------|
| Testes escritos | 0 | 0 | 21 | 29+ |
| Cobertura | 0% | 0% | 86% | 90%+ |
| CI configurado | ❌ | ❌ | ❌ | ✅ |

## Lições do Módulo de Testes

1. **Pirâmide de testes** - Mais unitários, menos E2E
2. **Pytest é simples** - `assert` e fixtures declarativas
3. **Mocks isolam** - Testes não precisam de externos
4. **TDD guia design** - Red → Green → Refactor
5. **CI automatiza** - Testes rodam em cada push
6. **Branch protection** - Código quebrado não entra

## Comandos Essenciais

```bash
# Rodar testes
pytest tests/ -v

# Com cobertura
pytest --cov=src --cov-report=html

# Verificar workflow
cat .github/workflows/ci.yml

# Push para disparar CI
git push origin main
```

# 12. Encerramento e gancho para a próxima aula (script)

Parabéns! Você completou o módulo de Testes Automatizados! Em 4 aulas você aprendeu:

- A pirâmide de testes e como planejar cobertura
- Pytest, fixtures e mocks
- Escrita prática de testes para código de Data Science
- CI com GitHub Actions e TDD

Seu projeto agora tem testes automatizados que rodam em cada push. Código quebrado não entra mais no main sem que você saiba. Isso é engenharia de software de verdade aplicada a Data Science.

Na próxima aula, vamos falar sobre **Docker e Ambientes Reprodutíveis**. Você vai aprender a containerizar sua aplicação para que ela rode exatamente igual em qualquer máquina - do seu notebook ao servidor de produção. Vamos criar um Dockerfile para a API de crédito e entender por que containers são essenciais para deploy de modelos.

O código está testado. Agora vamos garantir que o ambiente também seja consistente. Até a próxima aula!
