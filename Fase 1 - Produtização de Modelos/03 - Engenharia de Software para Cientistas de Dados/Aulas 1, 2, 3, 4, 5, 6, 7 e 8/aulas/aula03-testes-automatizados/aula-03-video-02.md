---
titulo: "Aula 03 – Parte 02: Frameworks de Teste e TDD - Garantindo Qualidade no Código DS"
modulo: "Engenharia de Software para Cientista de Dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 20
prerequisitos:
  - "Python 3.12+"
  - "UV instalado"
  - "Aula 03 - Parte 01 concluída"
  - "Repositório swe4ds-credit-api"
tags: ["pytest", "tdd", "test-driven-development", "fixtures", "mocks", "testes"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula, vamos conhecer as ferramentas que transformam a teoria de testes em prática. Vamos explorar o **Pytest** - o framework de testes mais poderoso e popular do ecossistema Python - e entender uma técnica que vai mudar sua forma de programar: o **TDD (Test-Driven Development)**.

Na aula anterior, entendemos POR QUE testar e QUAIS tipos de teste existem. Agora vamos aprender COMO testar de forma eficiente e elegante. O Pytest é tão intuitivo que você vai se perguntar por que não começou a usá-lo antes.

E o TDD? É uma técnica onde você escreve o teste ANTES do código. Parece estranho, mas ao final desta aula você vai entender por que grandes projetos de software adotam essa prática.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Você decide implementar testes no seu projeto de ML. Começa com a biblioteca `unittest` padrão do Python. O código de teste fica verboso: classes, métodos `setUp`, `tearDown`, asserções complexas. Para cada teste simples, você escreve 20 linhas de boilerplate. A motivação cai rapidamente.

**Agitação**: Os testes ficam tão complicados quanto o código que testam. Você precisa mockar uma API externa, mas a sintaxe é confusa. Fixtures são difíceis de compartilhar. Rodar testes específicos é trabalhoso. O que era para ajudar se torna mais uma fonte de frustração. Você começa a pular testes "por falta de tempo".

**Solução**: O Pytest simplifica tudo. Testes são funções simples com `assert`. Fixtures são declarativas e reutilizáveis. Mocks são intuitivos com `pytest-mock`. Rodar testes é `pytest`. Rodar um específico é `pytest test_file.py::test_name`. A barreira de entrada desaparece. Testar se torna natural e até prazeroso.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Instalar e configurar** Pytest em um projeto Python
2. **Escrever** testes simples usando asserções nativas
3. **Utilizar** fixtures para setup e teardown de testes
4. **Aplicar** mocks para simular dependências externas
5. **Explicar** o ciclo TDD: Red → Green → Refactor
6. **Avaliar** quando TDD é apropriado em projetos de Data Science

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Python 3.12+
- UV instalado
- Repositório `swe4ds-credit-api`
- Conceitos da Aula 03 - Parte 01

**Instalação do Pytest:**

```bash
# Navegar para o projeto
cd c:\Users\diogomiyake\projects\swe4ds-credit-api

# Ativar ambiente virtual
.venv\Scripts\activate

# Instalar Pytest e plugins úteis
uv pip install pytest pytest-cov pytest-mock

# Verificar instalação
pytest --version
```

**Saída esperada:**
```
pytest 8.x.x
```

**Atualizar requirements:**
```bash
uv pip freeze > requirements.txt
git add requirements.txt
git commit -m "chore: adiciona pytest e plugins de teste"
```

**Checklist de Setup:**
- [ ] Pytest instalado
- [ ] pytest-cov instalado (cobertura)
- [ ] pytest-mock instalado (mocking)
- [ ] Versão verificada

# 5. Visão geral do que já existe no projeto (continuidade)

**Estrutura atual:**
```
swe4ds-credit-api/
├── .git/
├── .dvc/
├── .gitignore
├── .venv/
├── LICENSE
├── README.md
├── requirements.txt       # Atualizado com pytest
├── data/
│   ├── raw/
│   └── processed/
├── models/
├── scripts/
│   └── download_data.py
└── src/
    ├── __init__.py
    └── data_loader.py
```

**O que faremos nesta aula:**
```
swe4ds-credit-api/
├── ...
├── pyproject.toml         # [NOVO] Configuração do pytest
├── tests/                 # [NOVO] Pasta de testes
│   ├── __init__.py
│   └── conftest.py        # [NOVO] Fixtures compartilhadas
└── ...
```

# 6. Passo a passo (comandos + código)

## Passo 1: Entendendo o Pytest (Excalidraw: Slide 4)

**Intenção**: Conhecer o framework antes de usá-lo.

### Por que Pytest?

O Pytest é o framework de testes mais popular em Python por várias razões:

1. **Sintaxe simples**: Use `assert` nativo do Python
2. **Descoberta automática**: Encontra testes por convenção de nomes
3. **Fixtures poderosas**: Setup reutilizável e declarativo
4. **Plugins ricos**: Cobertura, mocks, parametrização
5. **Output claro**: Mensagens de erro detalhadas

### Pytest vs Unittest

```python
# unittest (verboso)
import unittest

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
    
    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)
    
    def tearDown(self):
        del self.calc

# pytest (simples)
def test_add():
    calc = Calculator()
    assert calc.add(2, 3) == 5
```

Mesma funcionalidade, muito menos código!

**CHECKPOINT**: Você entende a vantagem de usar `assert` simples?

---

## Passo 2: Estrutura de um Teste Pytest

**Intenção**: Aprender a anatomia de um teste.

### Convenções de Nomenclatura

O Pytest descobre testes automaticamente seguindo convenções:

| Elemento | Convenção |
|----------|-----------|
| Arquivo | `test_*.py` ou `*_test.py` |
| Função | `test_*()` |
| Classe | `Test*` |
| Método | `test_*()` |

### Estrutura AAA (Arrange-Act-Assert)

Todo teste bem escrito segue este padrão:

```python
def test_preprocess_normalizes_features():
    # ARRANGE (preparar)
    df = pd.DataFrame({
        "feature1": [0, 50, 100],
        "target": [0, 1, 0]
    })
    
    # ACT (agir)
    result = normalize(df["feature1"])
    
    # ASSERT (verificar)
    assert result.min() == 0.0
    assert result.max() == 1.0
```

### Criando Estrutura de Testes

```bash
# Criar pasta de testes
mkdir tests

# Criar arquivos iniciais
# Windows PowerShell:
New-Item -Path "tests/__init__.py" -ItemType File
New-Item -Path "tests/conftest.py" -ItemType File

# Linux/macOS:
# touch tests/__init__.py tests/conftest.py
```

**CHECKPOINT**: Pasta `tests/` criada com `__init__.py` e `conftest.py`.

---

## Passo 3: Configurando Pytest (pyproject.toml)

**Intenção**: Configurar Pytest de forma moderna e centralizada.

Crie ou edite `pyproject.toml` na raiz do projeto:

```toml
# pyproject.toml

[project]
name = "swe4ds-credit-api"
version = "0.1.0"
description = "API REST para predição de inadimplência de cartão de crédito"
requires-python = ">=3.12"

[tool.pytest.ini_options]
# Diretório de testes
testpaths = ["tests"]

# Padrões de descoberta
python_files = ["test_*.py"]
python_functions = ["test_*"]
python_classes = ["Test*"]

# Opções de execução
addopts = [
    "-v",                    # Verbose
    "--tb=short",            # Traceback curto
    "--strict-markers",      # Markers devem ser registrados
]

# Markers customizados
markers = [
    "slow: marca testes lentos",
    "integration: marca testes de integração",
    "e2e: marca testes end-to-end",
]

[tool.coverage.run]
# Configuração de cobertura
source = ["src"]
omit = ["tests/*", "*/__init__.py"]

[tool.coverage.report]
# Relatório de cobertura
exclude_lines = [
    "pragma: no cover",
    "if __name__ == .__main__.:",
]
```

```bash
# Testar configuração
pytest --collect-only
```

**Saída esperada:**
```
collected 0 items
```

(Ainda não temos testes, mas a configuração está funcionando)

**CHECKPOINT**: `pytest --collect-only` executa sem erro.

---

## Passo 4: Fixtures - Setup Reutilizável (Excalidraw: Slide 4 - Fixtures)

**Intenção**: Aprender a criar setup compartilhado entre testes.

### O que são Fixtures?

**Fixtures** são funções que preparam dados ou recursos para testes. São como `setUp` do unittest, mas muito mais poderosas.

### Exemplo Básico

Edite `tests/conftest.py`:

```python
# tests/conftest.py
"""
Fixtures compartilhadas para todos os testes.

Fixtures definidas aqui ficam disponíveis automaticamente
em todos os arquivos de teste.
"""
import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def sample_credit_data():
    """
    Fixture que fornece um DataFrame de exemplo para testes.
    
    Returns:
        pd.DataFrame: Dataset pequeno simulando dados de crédito.
    """
    return pd.DataFrame({
        "ID": [1, 2, 3, 4, 5],
        "LIMIT_BAL": [50000, 100000, 30000, 80000, 60000],
        "SEX": [1, 2, 1, 2, 1],
        "EDUCATION": [2, 1, 3, 2, 1],
        "MARRIAGE": [1, 2, 1, 1, 2],
        "AGE": [25, 35, 28, 42, 31],
        "PAY_0": [0, -1, 2, 0, 1],
        "PAY_2": [0, -1, 2, 0, 0],
        "PAY_3": [0, -1, 0, 0, 0],
        "PAY_4": [0, 0, 0, 0, 0],
        "PAY_5": [0, 0, 0, 0, 0],
        "PAY_6": [0, 0, 0, 0, 0],
        "BILL_AMT1": [10000, 50000, 5000, 30000, 20000],
        "BILL_AMT2": [9000, 48000, 4500, 28000, 19000],
        "BILL_AMT3": [8500, 46000, 4000, 26000, 18000],
        "BILL_AMT4": [8000, 44000, 3500, 24000, 17000],
        "BILL_AMT5": [7500, 42000, 3000, 22000, 16000],
        "BILL_AMT6": [7000, 40000, 2500, 20000, 15000],
        "PAY_AMT1": [1000, 5000, 500, 3000, 2000],
        "PAY_AMT2": [1000, 5000, 500, 3000, 2000],
        "PAY_AMT3": [1000, 5000, 500, 3000, 2000],
        "PAY_AMT4": [1000, 5000, 500, 3000, 2000],
        "PAY_AMT5": [1000, 5000, 500, 3000, 2000],
        "PAY_AMT6": [1000, 5000, 500, 3000, 2000],
        "default payment next month": [0, 0, 1, 0, 1],
    })


@pytest.fixture
def sample_features():
    """
    Fixture com apenas features numéricas para teste de normalização.
    """
    return np.array([
        [50000, 25, 10000],
        [100000, 35, 50000],
        [30000, 28, 5000],
    ])


@pytest.fixture
def empty_dataframe():
    """
    Fixture com DataFrame vazio para testar edge cases.
    """
    return pd.DataFrame()
```

### Usando Fixtures

```python
# tests/unit/test_example.py
def test_sample_data_has_correct_columns(sample_credit_data):
    """
    Teste que usa a fixture sample_credit_data.
    
    A fixture é injetada automaticamente pelo nome do parâmetro.
    """
    expected_columns = ["ID", "LIMIT_BAL", "SEX", "EDUCATION"]
    for col in expected_columns:
        assert col in sample_credit_data.columns


def test_sample_data_has_five_rows(sample_credit_data):
    """Outro teste usando a mesma fixture."""
    assert len(sample_credit_data) == 5
```

### Escopos de Fixtures

| Escopo | Comportamento |
|--------|---------------|
| `function` (padrão) | Criada para cada teste |
| `class` | Criada uma vez por classe |
| `module` | Criada uma vez por arquivo |
| `session` | Criada uma vez por execução |

```python
@pytest.fixture(scope="module")
def expensive_resource():
    """Recurso caro, criado uma vez por módulo."""
    return load_large_model()
```

**CHECKPOINT**: Você entende como fixtures são injetadas automaticamente?

---

## Passo 5: Mocks - Simulando Dependências (Excalidraw: Slide 6)

**Intenção**: Aprender a isolar testes de dependências externas.

### O que são Mocks?

**Mocks** são objetos falsos que simulam comportamento de dependências reais:
- APIs externas
- Banco de dados
- Arquivos
- Serviços de terceiros

### Por que Mockar?

```python
# SEM MOCK - depende de arquivo real (frágil)
def test_load_data():
    df = load_credit_data(Path("data/raw/credit.csv"))  # Arquivo pode não existir!
    assert len(df) > 0

# COM MOCK - isolado e confiável
def test_load_data(mocker):
    mock_df = pd.DataFrame({"col": [1, 2, 3]})
    mocker.patch("src.data_loader.pd.read_csv", return_value=mock_df)
    
    df = load_credit_data(Path("qualquer_caminho.csv"))
    assert len(df) == 3
```

### Usando pytest-mock

```python
# tests/unit/test_data_loader.py
import pytest
from pathlib import Path


def test_load_credit_data_from_cache(mocker, tmp_path):
    """
    Testa que load_credit_data usa cache quando disponível.
    
    Args:
        mocker: Fixture do pytest-mock para criar mocks.
        tmp_path: Fixture built-in para diretório temporário.
    """
    # ARRANGE
    # Criar mock de pd.read_parquet
    mock_df = pd.DataFrame({"test": [1, 2, 3]})
    mock_read_parquet = mocker.patch(
        "src.data_loader.pd.read_parquet",
        return_value=mock_df
    )
    
    # Criar arquivo de cache fake
    cache_path = tmp_path / "data" / "credit_data.parquet"
    cache_path.parent.mkdir(parents=True)
    cache_path.touch()
    
    # Mockar Path.exists para retornar True
    mocker.patch.object(Path, "exists", return_value=True)
    
    # ACT
    # Chamar função (implementação real, dependências mockadas)
    # result = load_credit_data(use_cache=True)
    
    # ASSERT
    # mock_read_parquet.assert_called_once()
    # assert result.equals(mock_df)
    pass  # Implementaremos na próxima aula


def test_load_credit_data_handles_missing_file(mocker):
    """
    Testa que load_credit_data levanta erro para arquivo inexistente.
    """
    mocker.patch.object(Path, "exists", return_value=False)
    
    # with pytest.raises(FileNotFoundError):
    #     load_credit_data(filepath=Path("nao_existe.csv"))
    pass  # Implementaremos na próxima aula
```

### Padrões Comuns de Mock

```python
# Mock de retorno simples
mocker.patch("module.function", return_value=42)

# Mock que levanta exceção
mocker.patch("module.function", side_effect=ValueError("Erro!"))

# Mock com múltiplos retornos
mocker.patch("module.function", side_effect=[1, 2, 3])

# Verificar se foi chamado
mock = mocker.patch("module.function")
# ... código que chama a função ...
mock.assert_called_once_with(expected_arg)
```

**CHECKPOINT**: Você entende por que mocks são essenciais para testes unitários?

---

## Passo 6: Test-Driven Development (TDD) (Excalidraw: Slide 5)

**Intenção**: Aprender a técnica de escrever testes antes do código.

### O Ciclo TDD: Red → Green → Refactor

```
┌─────────────────────────────────────────────────────────────────┐
│                      CICLO TDD                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│         ┌─────────┐                                             │
│         │  RED    │  1. Escreva um teste que FALHA              │
│         │ (Falha) │                                             │
│         └────┬────┘                                             │
│              │                                                  │
│              ▼                                                  │
│         ┌─────────┐                                             │
│         │  GREEN  │  2. Escreva código MÍNIMO para passar       │
│         │ (Passa) │                                             │
│         └────┬────┘                                             │
│              │                                                  │
│              ▼                                                  │
│         ┌──────────┐                                            │
│         │ REFACTOR │  3. Melhore o código (testes continuam     │
│         │(Melhora) │     passando)                              │
│         └────┬─────┘                                            │
│              │                                                  │
│              └──────────────► Repita                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Exemplo Prático de TDD

Vamos criar uma função de validação usando TDD:

**1. RED - Escrever teste que falha:**

```python
# tests/unit/test_validation.py
def test_validate_age_rejects_negative():
    """Idade negativa deve ser rejeitada."""
    from src.validation import validate_age
    
    result = validate_age(-5)
    assert result is False


def test_validate_age_accepts_valid():
    """Idade válida deve ser aceita."""
    from src.validation import validate_age
    
    result = validate_age(25)
    assert result is True
```

Rodamos: `pytest tests/unit/test_validation.py`

Resultado: **FALHA** (módulo não existe ainda)

**2. GREEN - Código mínimo para passar:**

```python
# src/validation.py
def validate_age(age: int) -> bool:
    """Valida se idade é aceitável."""
    return age >= 0
```

Rodamos: `pytest tests/unit/test_validation.py`

Resultado: **PASSA**

**3. REFACTOR - Melhorar mantendo testes:**

```python
# src/validation.py
def validate_age(age: int) -> bool:
    """
    Valida se idade é aceitável para análise de crédito.
    
    Args:
        age: Idade em anos.
        
    Returns:
        True se idade é válida (18-100), False caso contrário.
    """
    MIN_AGE = 18
    MAX_AGE = 100
    return MIN_AGE <= age <= MAX_AGE
```

Adicionamos mais testes para a nova lógica, e o ciclo continua.

### Benefícios do TDD

1. **Design guiado por uso**: Você pensa na interface antes da implementação
2. **Cobertura garantida**: Todo código nasce com teste
3. **Documentação viva**: Testes mostram como usar
4. **Refatoração segura**: Testes protegem contra regressões

### TDD em Data Science: Quando Aplicar

| Bom para TDD | Não ideal para TDD |
|--------------|-------------------|
| Funções de validação | Treinamento de modelos |
| Preprocessamento | Análise exploratória |
| Formatação de output | Visualizações |
| Lógica de negócio | Notebooks de pesquisa |

**CHECKPOINT**: Você consegue explicar as 3 fases do ciclo TDD?

---

## Passo 7: Estrutura Final para Testes

**Intenção**: Deixar projeto pronto para implementação prática.

```bash
# Criar estrutura completa de testes
mkdir -p tests/unit tests/integration tests/e2e

# Criar __init__.py em cada pasta
# Windows PowerShell:
New-Item -Path "tests/unit/__init__.py" -ItemType File
New-Item -Path "tests/integration/__init__.py" -ItemType File
New-Item -Path "tests/e2e/__init__.py" -ItemType File

# Linux/macOS:
# touch tests/unit/__init__.py tests/integration/__init__.py tests/e2e/__init__.py
```

**Estrutura resultante:**
```
tests/
├── __init__.py
├── conftest.py           # Fixtures compartilhadas
├── unit/
│   ├── __init__.py
│   ├── test_data_loader.py   # (próxima aula)
│   └── test_validation.py    # (próxima aula)
├── integration/
│   ├── __init__.py
│   └── test_pipeline.py      # (futuro)
└── e2e/
    ├── __init__.py
    └── test_api.py           # (futuro)
```

```bash
# Commit da estrutura
git add tests/ pyproject.toml
git commit -m "feat: configura estrutura de testes com pytest

- Adiciona pyproject.toml com configuração pytest
- Cria estrutura de pastas tests/
- Adiciona fixtures básicas em conftest.py"
```

**CHECKPOINT**: Estrutura de testes criada e commitada.

# 7. Testes rápidos e validação

**Verificar Pytest funciona:**
```bash
pytest --collect-only
```

Esperado: Lista estrutura (0 items por enquanto).

**Criar teste mínimo para validar:**

```python
# tests/unit/test_sanity.py
def test_sanity_check():
    """Teste mínimo para verificar que pytest funciona."""
    assert 1 + 1 == 2


def test_python_version():
    """Verifica versão do Python."""
    import sys
    assert sys.version_info >= (3, 12)
```

```bash
pytest tests/unit/test_sanity.py -v
```

**Esperado:**
```
tests/unit/test_sanity.py::test_sanity_check PASSED
tests/unit/test_sanity.py::test_python_version PASSED
```

# 8. Observabilidade e boas práticas (mini-bloco)

### Boas Práticas Aplicadas

1. **Configuração em pyproject.toml**
   - Centraliza configuração do projeto
   - Padrão moderno do Python
   - **Trade-off**: Arquivo maior, mas tudo em um lugar

2. **Fixtures em conftest.py**
   - Reutilização automática
   - Separação de concerns
   - **Trade-off**: Pode ficar grande; divida por módulo se necessário

3. **Nomenclatura descritiva**
   - `test_validate_age_rejects_negative` > `test_1`
   - Facilita identificar falhas
   - **Trade-off**: Nomes longos, mas auto-documentados

4. **Mocks para isolamento**
   - Testes não dependem de externos
   - Execução rápida e confiável
   - **Trade-off**: Mocks podem divergir da realidade

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| `ModuleNotFoundError: No module named 'src'` | Python path incorreto | Adicione `pythonpath = ["."]` ao pyproject.toml |
| `fixture 'X' not found` | Fixture não definida ou nome errado | Verifique conftest.py e nome do parâmetro |
| `PytestUnknownMarkWarning` | Marker não registrado | Adicione ao `[tool.pytest.ini_options]` |
| Teste não descoberto | Nome não segue convenção | Use `test_*.py` e `def test_*()` |
| Mock não funciona | Caminho de patch incorreto | Patch onde é usado, não onde é definido |
| Fixture não injetada | Esqueceu parâmetro na função | Adicione nome da fixture como parâmetro |

# 10. Exercícios (básico e avançado)

## Exercício Básico 1: Criar Fixture

Crie uma fixture chamada `sample_predictions` que retorna:
```python
[0, 1, 0, 1, 1, 0, 0, 1]
```

Use-a em um teste que verifica se a lista tem 8 elementos.

**Critério de sucesso**: Teste passa com `pytest -v`.

## Exercício Básico 2: Teste com Parametrização

Crie um teste parametrizado para validar idades:

```python
@pytest.mark.parametrize("age,expected", [
    (25, True),
    (-1, False),
    (150, False),
    (18, True),
])
def test_validate_age_cases(age, expected):
    # Implemente
    pass
```

**Critério de sucesso**: Todos os 4 casos passam.

## Exercício Avançado: TDD Completo

Use TDD para criar `src/validation.py` com:

1. `validate_limit_bal(value)`: Retorna True se 0 < value < 1_000_000
2. `validate_education(value)`: Retorna True se value in [1, 2, 3, 4]

Siga o ciclo Red → Green → Refactor para cada função.

**Critério de sucesso**: 
- Pelo menos 4 testes por função
- Cobertura de 100% nas funções criadas

# 11. Resultados e Lições

## Como Medir Sucesso

| Métrica | Como Medir | Valor Esperado |
|---------|------------|----------------|
| Pytest funcionando | `pytest --version` | Versão 8.x |
| Estrutura criada | `ls tests/` | unit/, integration/, e2e/ |
| Configuração OK | `pytest --collect-only` | Sem erros |
| Testes passando | `pytest tests/unit/test_sanity.py` | 2 passed |

## Lições Aprendidas

1. **Pytest simplifica testes** - menos boilerplate, mais produtividade
2. **Fixtures são poderosas** - setup reutilizável e declarativo
3. **Mocks isolam dependências** - testes rápidos e confiáveis
4. **TDD guia o design** - pense no uso antes da implementação
5. **Configuração centralizada** - pyproject.toml é o padrão moderno

# 12. Encerramento e gancho para a próxima aula (script)

Perfeito! Agora você conhece o Pytest e está pronto para escrever testes de verdade. Você entende fixtures, mocks, e o ciclo TDD. A estrutura do projeto está preparada.

Na próxima aula, vamos colocar tudo isso em prática. Vamos escrever testes unitários reais para o nosso `data_loader.py`. Você vai ver o Pytest em ação, testando funções de preprocessamento de dados, validação de inputs, e tratamento de erros.

Será uma aula intensamente prática. Prepare-se para escrever código - tanto testes quanto as funções que eles testam. Vamos usar TDD para criar uma função de validação completa para nossa API de crédito.

Até a próxima aula!
