---
titulo: "Aula 05 – Parte 03: Hands-on - Configurando Ambiente e Fixando Dependências"
modulo: "Engenharia de Software para Cientista de Dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 25
prerequisitos:
  - "Python 3.12+"
  - "UV instalado"
  - "Aula 05 - Partes 01 e 02 concluídas"
tags: ["taskipy", "pytest", "ruff", "workflow", "automation"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula vamos integrar três ferramentas que vão transformar seu workflow de desenvolvimento: **Taskipy**, **Pytest** e **Ruff**.

Até agora você sabe criar ambientes e gerenciar pacotes. Mas no dia a dia, você precisa rodar testes, formatar código, fazer lint, tudo repetidamente. Digitar `uv run pytest tests/ -v --cov=src --cov-report=html` toda vez é cansativo e propenso a erros.

Taskipy resolve isso: você define aliases no `pyproject.toml` e roda `task test`. Simples assim. Junto com Ruff (linter e formatador ultrarrápido) e Pytest (framework de testes), você terá um ambiente de desenvolvimento profissional.

Vamos configurar tudo isso no nosso projeto de crédito e criar um workflow integrado que você vai usar todos os dias.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Você trabalha no projeto de crédito. Precisa rodar testes, verificar estilo de código, formatar arquivos. Cada tarefa é um comando diferente com flags específicas. Você esquece as flags, digita errado, perde tempo.

**Agitação**: `pytest tests/ -v --cov=src --cov-report=html --cov-fail-under=80`. Você digita isso 20 vezes por dia. Um dia esquece o `--cov-fail-under`, o código vai para produção com 30% de cobertura. O linter? `ruff check src/ --fix`. Mas e o formatador? `ruff format src/`. São 3 comandos diferentes. O novo estagiário não sabe nenhum deles. A documentação está desatualizada.

**Solução**: Taskipy. Você define uma vez no `pyproject.toml`:
```toml
[tool.taskipy.tasks]
test = "pytest tests/ -v --cov=src"
lint = "ruff check src/"
format = "ruff format src/"
```

Agora é só `task test`, `task lint`, `task format`. Todo mundo usa o mesmo comando. Impossível esquecer flags. Documentação viva no próprio código.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Configurar** Taskipy para automação de tarefas
2. **Integrar** Pytest com cobertura de código
3. **Configurar** Ruff como linter e formatador
4. **Criar** scripts reutilizáveis no pyproject.toml
5. **Executar** workflow completo com um comando
6. **Aplicar** boas práticas de qualidade de código

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Ambiente virtual ativado
- UV configurado com pyproject.toml

**Verificar ambiente:**

```bash
# Navegar para o projeto
cd c:\Users\diogomiyake\projects\swe4ds-credit-api

# Ativar ambiente
.\.venv\Scripts\Activate.ps1

# Verificar UV
uv --version

# Verificar que pyproject.toml existe
cat pyproject.toml | head -20
```

**Checklist:**
- [ ] Ambiente virtual ativado
- [ ] pyproject.toml existente
- [ ] UV funcionando

# 5. Visão geral do que já existe no projeto (continuidade)

**Estado atual:**
```
swe4ds-credit-api/
├── .venv/
├── pyproject.toml              # Com dependências básicas
├── uv.lock
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   └── validation.py
└── tests/
    ├── __init__.py
    └── test_validation.py
```

**O que vamos configurar:**
```
pyproject.toml
├── [tool.taskipy.tasks]        # [NOVO] Scripts de automação
├── [tool.pytest.ini_options]   # [NOVO] Configuração pytest
└── [tool.ruff]                 # [NOVO] Configuração ruff
```

# 6. Passo a passo (comandos + código)

## Passo 1: Instalando Ferramentas de Desenvolvimento (Excalidraw: Slide 5)

**Intenção**: Adicionar taskipy, pytest e ruff como dependências de desenvolvimento.

```bash
# Adicionar ferramentas de desenvolvimento
uv add --dev taskipy pytest pytest-cov ruff

# Verificar instalação
uv pip list | grep -E "taskipy|pytest|ruff"
```

**Saída esperada:**
```
taskipy     1.13.0
pytest      8.3.4
pytest-cov  6.0.0
ruff        0.9.2
```

### O que cada ferramenta faz

| Ferramenta | Propósito |
|------------|-----------|
| **taskipy** | Task runner - aliases para comandos |
| **pytest** | Framework de testes |
| **pytest-cov** | Plugin de cobertura para pytest |
| **ruff** | Linter + Formatador (substitui flake8, black, isort) |

**CHECKPOINT**: Todas as ferramentas instaladas (`uv pip list` mostra todas).

---

## Passo 2: Configurando Taskipy (Excalidraw: Slide 5)

**Intenção**: Criar aliases para comandos frequentes.

Abra o arquivo e aplique o **diff lógico** abaixo (copie exatamente o bloco):

```bash
# Abrir o arquivo
code pyproject.toml
```

```toml
# (ADICIONAR ao final do arquivo)
[tool.taskipy.tasks]
test = "pytest tests/ -v"
test-cov = "pytest tests/ -v --cov=src --cov-report=html --cov-report=term"
lint = "ruff check src/ tests/"
lint-fix = "ruff check src/ tests/ --fix"
format = "ruff format src/ tests/"
format-check = "ruff format src/ tests/ --check"
check = "task lint && task format-check && task test"
clean = "rm -rf .pytest_cache .coverage htmlcov __pycache__ .ruff_cache"
```

Se preferir, **substitua/adicione** a seção manualmente. O objetivo é que o arquivo fique com esta seção presente:

```toml
# =============================================================================
# TASKIPY - Automação de Tarefas
# =============================================================================
[tool.taskipy.tasks]
# Testes
test = "pytest tests/ -v"
test-cov = "pytest tests/ -v --cov=src --cov-report=html --cov-report=term"

# Qualidade de código
lint = "ruff check src/ tests/"
lint-fix = "ruff check src/ tests/ --fix"
format = "ruff format src/ tests/"
format-check = "ruff format src/ tests/ --check"

# Verificação completa (rodar antes de commit)
check = "task lint && task format-check && task test"

# Limpeza
clean = "rm -rf .pytest_cache .coverage htmlcov __pycache__ .ruff_cache"
```

### Usando Taskipy

```bash
# Ver tarefas disponíveis
task --list

# Rodar testes
task test

# Rodar lint
task lint

# Verificação completa
task check
```

**Saída do `task --list`:**
```
test        pytest tests/ -v
test-cov    pytest tests/ -v --cov=src --cov-report=html --cov-report=term
lint        ruff check src/ tests/
lint-fix    ruff check src/ tests/ --fix
format      ruff format src/ tests/
format-check ruff format src/ tests/ --check
check       task lint && task format-check && task test
clean       rm -rf .pytest_cache .coverage htmlcov __pycache__ .ruff_cache
```

**CHECKPOINT**: `task --list` mostra todas as tarefas configuradas.

---

## Passo 3: Configurando Pytest (Excalidraw: Slide 5)

**Intenção**: Definir configurações padrão para pytest.

Abra o `pyproject.toml` e **cole o bloco completo** abaixo (mão na massa):

```toml
# =============================================================================
# PYTEST - Configuração de Testes
# =============================================================================
[tool.pytest.ini_options]
# Diretório de testes
testpaths = ["tests"]

# Opções padrão
addopts = [
    "-v",                    # Verbose
    "--strict-markers",      # Markers devem ser declarados
    "--tb=short",            # Traceback curto
]

# Markers personalizados
markers = [
    "slow: testes lentos (rodar com -m 'not slow' para pular)",
    "integration: testes de integração",
]

# Padrão de arquivos de teste
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

# =============================================================================
# COVERAGE - Configuração de Cobertura
# =============================================================================
[tool.coverage.run]
source = ["src"]
branch = true
omit = [
    "*/tests/*",
    "*/__pycache__/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
]
fail_under = 70
show_missing = true
```

### Testando a Configuração

```bash
# Rodar testes (usa configuração do pyproject.toml)
task test

# Rodar com cobertura
task test-cov
```

**Saída esperada:**
```
========================= test session starts ==========================
platform win32 -- Python 3.12.x, pytest-8.x.x
rootdir: C:\Users\diogomiyake\projects\swe4ds-credit-api
configfile: pyproject.toml
plugins: cov-6.0.0
collected X items

tests/test_validation.py::test_validate_limit_bal_valid PASSED
tests/test_validation.py::test_validate_limit_bal_invalid PASSED
...

========================== X passed in 0.XXs ===========================
```

**CHECKPOINT**: `task test` roda testes com configurações do pyproject.toml.

---

## Passo 4: Configurando Ruff (Excalidraw: Slide 6)

**Intenção**: Configurar linter e formatador unificados.

No mesmo arquivo, **adicione a seção do Ruff** (copie e cole):

```toml
# =============================================================================
# RUFF - Linter e Formatador
# =============================================================================
[tool.ruff]
# Versão do Python alvo
target-version = "py312"

# Tamanho máximo de linha
line-length = 88

# Diretórios a verificar
src = ["src", "tests"]

# Arquivos/pastas a ignorar
exclude = [
    ".git",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "*.egg-info",
]

[tool.ruff.lint]
# Regras a habilitar
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes
    "I",      # isort (ordenação de imports)
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
    "SIM",    # flake8-simplify
]

# Regras a ignorar
ignore = [
    "E501",   # line too long (formatador cuida)
    "B008",   # function call in argument defaults
]

# Permitir correção automática para todas as regras habilitadas
fixable = ["ALL"]
unfixable = []

[tool.ruff.lint.per-file-ignores]
# Testes podem ter imports não usados (fixtures)
"tests/*" = ["F401"]

[tool.ruff.lint.isort]
# Configuração do ordenador de imports
known-first-party = ["src"]

[tool.ruff.format]
# Estilo de aspas
quote-style = "double"

# Indentação
indent-style = "space"

# Final de linha
line-ending = "auto"
```

### O que o Ruff verifica

| Código | Categoria | Exemplo |
|--------|-----------|---------|
| E | Erros de estilo | Indentação errada |
| W | Warnings de estilo | Espaços em branco no final |
| F | Pyflakes | Variável não usada |
| I | isort | Imports fora de ordem |
| B | Bugbear | Bugs comuns |
| UP | pyupgrade | Sintaxe antiga do Python |

### Testando Ruff

```bash
# Verificar código
task lint

# Corrigir automaticamente
task lint-fix

# Formatar código
task format

# Verificar formatação (sem modificar)
task format-check
```

**Saída do lint (se houver problemas):**
```
src/data_loader.py:10:1: I001 Import block is un-sorted or un-formatted
src/validation.py:5:5: F841 Local variable `x` is assigned to but never used
Found 2 errors.
```

**CHECKPOINT**: `task lint` e `task format` funcionam corretamente.

---

## Passo 5: Criando Arquivo de Exemplo para Testar

**Intenção**: Ter código para verificar as ferramentas.

Vamos verificar se `src/validation.py` existe e está correto:

```bash
# Verificar conteúdo atual
cat src/validation.py
```

Se precisar atualizar, o arquivo deve estar assim:

```python
# src/validation.py
"""
Módulo de validação de dados para análise de crédito.

Este módulo contém funções para validar os dados de entrada
da API de análise de crédito.
"""

from typing import Any


def validate_limit_bal(limit_bal: float) -> bool:
    """
    Valida o limite de crédito.

    Args:
        limit_bal: Valor do limite de crédito em NT$.

    Returns:
        True se o valor é válido (positivo), False caso contrário.

    Examples:
        >>> validate_limit_bal(50000)
        True
        >>> validate_limit_bal(-1000)
        False
    """
    return limit_bal > 0


def validate_age(age: int) -> bool:
    """
    Valida a idade do cliente.

    Args:
        age: Idade em anos.

    Returns:
        True se a idade está no range válido (18-120), False caso contrário.
    """
    return 18 <= age <= 120


def validate_education(education: int) -> bool:
    """
    Valida o nível educacional.

    Args:
        education: Código do nível educacional (1-4).

    Returns:
        True se o código é válido, False caso contrário.
    """
    valid_codes = {1, 2, 3, 4}  # 1=graduate, 2=university, 3=high school, 4=others
    return education in valid_codes


def validate_input(data: dict[str, Any]) -> dict[str, list[str]]:
    """
    Valida todos os campos de entrada.

    Args:
        data: Dicionário com os dados do cliente.

    Returns:
        Dicionário com lista de erros por campo.
    """
    errors: dict[str, list[str]] = {}

    if "LIMIT_BAL" in data and not validate_limit_bal(data["LIMIT_BAL"]):
        errors.setdefault("LIMIT_BAL", []).append("Limite deve ser positivo")

    if "AGE" in data and not validate_age(data["AGE"]):
        errors.setdefault("AGE", []).append("Idade deve estar entre 18 e 120")

    if "EDUCATION" in data and not validate_education(data["EDUCATION"]):
        errors.setdefault("EDUCATION", []).append("Educação deve ser 1, 2, 3 ou 4")

    return errors
```

**CHECKPOINT**: `src/validation.py` existe e tem código válido.

---

## Passo 6: Adicionando Mais Testes

**Intenção**: Ter testes suficientes para demonstrar cobertura.

Atualize `tests/test_validation.py`:

```python
# tests/test_validation.py
"""
Testes para o módulo de validação.
"""

import pytest

from src.validation import (
    validate_age,
    validate_education,
    validate_input,
    validate_limit_bal,
)


class TestValidateLimitBal:
    """Testes para validate_limit_bal."""

    def test_valid_positive_limit(self):
        """Limite positivo deve ser válido."""
        assert validate_limit_bal(50000) is True

    def test_valid_small_limit(self):
        """Limite pequeno mas positivo deve ser válido."""
        assert validate_limit_bal(1) is True

    def test_invalid_zero_limit(self):
        """Limite zero deve ser inválido."""
        assert validate_limit_bal(0) is False

    def test_invalid_negative_limit(self):
        """Limite negativo deve ser inválido."""
        assert validate_limit_bal(-1000) is False


class TestValidateAge:
    """Testes para validate_age."""

    def test_valid_adult_age(self):
        """Idade de adulto deve ser válida."""
        assert validate_age(30) is True

    def test_valid_minimum_age(self):
        """Idade mínima (18) deve ser válida."""
        assert validate_age(18) is True

    def test_valid_maximum_age(self):
        """Idade máxima (120) deve ser válida."""
        assert validate_age(120) is True

    def test_invalid_minor_age(self):
        """Idade de menor deve ser inválida."""
        assert validate_age(17) is False

    def test_invalid_too_old(self):
        """Idade acima de 120 deve ser inválida."""
        assert validate_age(121) is False


class TestValidateEducation:
    """Testes para validate_education."""

    @pytest.mark.parametrize("code", [1, 2, 3, 4])
    def test_valid_education_codes(self, code):
        """Códigos 1-4 devem ser válidos."""
        assert validate_education(code) is True

    @pytest.mark.parametrize("code", [0, 5, -1, 100])
    def test_invalid_education_codes(self, code):
        """Códigos fora de 1-4 devem ser inválidos."""
        assert validate_education(code) is False


class TestValidateInput:
    """Testes para validate_input."""

    def test_valid_complete_input(self):
        """Input completo e válido não deve ter erros."""
        data = {"LIMIT_BAL": 50000, "AGE": 30, "EDUCATION": 2}
        errors = validate_input(data)
        assert errors == {}

    def test_invalid_limit_bal(self):
        """Input com limite inválido deve retornar erro."""
        data = {"LIMIT_BAL": -1000}
        errors = validate_input(data)
        assert "LIMIT_BAL" in errors

    def test_multiple_errors(self):
        """Input com múltiplos erros deve retornar todos."""
        data = {"LIMIT_BAL": -1000, "AGE": 15, "EDUCATION": 0}
        errors = validate_input(data)
        assert len(errors) == 3

    def test_empty_input(self):
        """Input vazio não deve ter erros."""
        data = {}
        errors = validate_input(data)
        assert errors == {}
```

**CHECKPOINT**: Arquivo de testes atualizado.

---

## Passo 7: Rodando Workflow Completo (Excalidraw: Slide 6)

**Intenção**: Executar todas as verificações de uma vez.

```bash
# Rodar verificação completa
task check
```

**Saída esperada:**
```
# Lint
All checks passed!

# Format check
12 files already formatted

# Test
========================= test session starts ==========================
...
tests/test_validation.py ............                            [100%]
========================== 12 passed in 0.XXs ==========================
```

### Rodar com Cobertura

```bash
# Testes com cobertura
task test-cov
```

**Saída esperada:**
```
========================= test session starts ==========================
...
tests/test_validation.py ............                            [100%]

---------- coverage: platform win32, python 3.12.x -----------
Name                  Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------------------
src/__init__.py           0      0      0      0   100%
src/data_loader.py       XX      X      X      X    XX%   XX-XX
src/validation.py        25      0     10      0   100%
-----------------------------------------------------------------
TOTAL                    XX      X     XX      X    XX%

========================== 12 passed in 0.XXs ==========================
```

**CHECKPOINT**: `task check` passa sem erros. Cobertura gerada.

---

## Passo 8: Visualizando Relatório de Cobertura

**Intenção**: Ver cobertura detalhada em HTML.

```bash
# Gerar relatório HTML
task test-cov

# Abrir relatório (Windows)
start htmlcov/index.html

# Ou navegar manualmente para htmlcov/index.html
```

O relatório HTML mostra:
- Porcentagem de cobertura por arquivo
- Linhas cobertas (verde)
- Linhas não cobertas (vermelho)
- Branches cobertos/não cobertos

**CHECKPOINT**: Relatório HTML acessível em `htmlcov/index.html`.

---

## Passo 9: Commit das Configurações

**Intenção**: Versionar todas as configurações.

```bash
# Verificar mudanças
git status

# Adicionar arquivos
git add pyproject.toml uv.lock src/ tests/

# Commit
git commit -m "feat: configura ferramentas de desenvolvimento

Adiciona e configura:
- Taskipy: automação de tarefas (test, lint, format, check)
- Pytest: framework de testes com cobertura
- Ruff: linter e formatador unificado

Scripts disponíveis:
- task test: rodar testes
- task test-cov: testes com cobertura
- task lint: verificar código
- task format: formatar código
- task check: verificação completa"

# Push
git push origin main
```

**CHECKPOINT**: Configurações versionadas no git.

# 7. Testes rápidos e validação

```bash
# Verificar que todas as tarefas existem
task --list

# Rodar lint
task lint

# Rodar formatação
task format

# Rodar testes
task test

# Rodar verificação completa
task check

# Rodar testes com cobertura
task test-cov

# Verificar que relatório foi gerado
ls htmlcov/
```

**Todos os comandos devem executar sem erros.**

# 8. Observabilidade e boas práticas (mini-bloco)

### Boas Práticas de Workflow de Desenvolvimento

1. **`task check` antes de cada commit**
   - Garante que código passa em lint, format e tests
   - Previne CI failures
   - **Trade-off**: Adiciona ~10 segundos ao commit, mas economiza tempo de CI

2. **Cobertura mínima obrigatória**
   - Configure `fail_under = 70` ou mais
   - Impede regressão de cobertura
   - **Trade-off**: Pode bloquear código urgente, mas mantém qualidade

3. **Ruff em vez de múltiplas ferramentas**
   - Substitui: flake8, black, isort, pyupgrade
   - Mais rápido e configuração unificada
   - **Trade-off**: Menos customização, mas mais simplicidade

4. **Scripts documentados no pyproject.toml**
   - Todo mundo usa os mesmos comandos
   - Novos membros aprendem rápido (`task --list`)
   - **Trade-off**: Mais configuração inicial, mas onboarding mais fácil

5. **Pre-commit hooks (próximo passo)**
   - Automatiza `task check` antes de cada commit
   - Impossível commitar código quebrado
   - **Trade-off**: Pode frustrar em emergências

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| `task: command not found` | Taskipy não instalado | `uv add --dev taskipy` |
| `No module named 'src'` | Estrutura de imports errada | Verificar `__init__.py` em `src/` |
| Ruff mostra muitos erros | Código legado | `task lint-fix` para correção automática |
| Cobertura abaixo do mínimo | Testes insuficientes | Adicionar testes ou ajustar `fail_under` |
| Import error nos testes | Ambiente não sincronizado | `uv sync --dev` |
| pytest não encontra testes | Nome de arquivo errado | Arquivos devem começar com `test_` |

# 10. Exercícios (básico e avançado)

## Exercício Básico 1: Adicionar Nova Tarefa

Crie uma tarefa chamada `docs` que gera documentação (por enquanto, pode ser um `echo "Documentação gerada"`). Teste com `task docs`.

**Critério de sucesso**: `task --list` mostra `docs` e `task docs` executa.

## Exercício Básico 2: Aumentar Cobertura

Adicione testes para `data_loader.py` até atingir pelo menos 80% de cobertura total. Use `task test-cov` para verificar.

**Critério de sucesso**: Cobertura total >= 80%.

## Exercício Avançado: Pre-commit Hooks

Pesquise e configure o `pre-commit` para rodar `task check` automaticamente antes de cada commit. Dica: crie `.pre-commit-config.yaml`.

**Critério de sucesso**: Tentar commitar código com erro de lint falha automaticamente.

# 11. Resultados e Lições

## Métricas para Acompanhar

| Métrica | Como medir | Valor esperado |
|---------|------------|----------------|
| Tempo do `task check` | `Measure-Command { task check }` | < 15 segundos |
| Cobertura de código | `task test-cov` | >= 70% |
| Erros de lint | `task lint` | 0 erros |
| Arquivos não formatados | `task format-check` | 0 arquivos |

## Lições desta Aula

1. **Automação economiza tempo** - `task test` vs digitar comando longo
2. **Consistência importa** - Todo mundo usa os mesmos comandos
3. **Ruff é moderno** - Substitui múltiplas ferramentas
4. **Cobertura é métrica** - Não é garantia de qualidade, mas ajuda
5. **pyproject.toml centraliza tudo** - Uma fonte de verdade

# 12. Encerramento e gancho para a próxima aula (script)

Parabéns! Agora você tem um ambiente de desenvolvimento profissional configurado. Com `task test`, `task lint`, `task format` e `task check`, você tem controle total sobre a qualidade do código.

Seu workflow agora é:
1. Escreve código
2. `task format` - formata
3. `task lint` - verifica problemas
4. `task test` - roda testes
5. `task check` - verificação final
6. Commit!

Na próxima e última aula deste módulo, vamos aprender a **empacotar código reutilizável**. Você vai entender como transformar seu projeto em um pacote Python que pode ser instalado com `pip install`. Vamos falar sobre `setup.py`, estrutura de pacotes, e quando vale a pena empacotar.

Até a próxima aula!
