---
titulo: "Aula 03 – Parte 03: Hands-on Pytest - Testando Código de Data Science"
modulo: "Engenharia de Software para Cientista de Dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 25
prerequisitos:
  - "Python 3.12+"
  - "UV instalado"
  - "Aula 03 - Partes 01 e 02 concluídas"
  - "Repositório swe4ds-credit-api com pytest configurado"
tags: ["pytest", "hands-on", "parametrize", "testes-unitarios", "data-loader"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Chegou a hora de colocar a mão na massa! Nas aulas anteriores, entendemos a teoria dos testes e conhecemos o Pytest. Agora vamos escrever testes de verdade para o nosso código de Data Science.

Essa é a aula mais longa do módulo - 25 minutos - porque quero que vocês vejam todo o fluxo na prática. Vamos testar o `data_loader.py` que criamos nas aulas de Git. Você vai aprender a usar `pytest.mark.parametrize`, testar edge cases, e medir cobertura de código.

Acompanhe digitando junto. Escrever testes é uma habilidade que só se desenvolve praticando. Ao final desta aula, você terá testes reais funcionando no seu projeto.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Você tem um `data_loader.py` funcionando. Carrega dados, preprocessa features, extrai nomes de colunas. Mas como saber se funciona para todos os casos? Você testou manualmente uma vez e assumiu que está OK.

**Agitação**: Semanas depois, você adiciona uma feature nova. O código quebra silenciosamente - `load_credit_data` agora retorna dados com colunas faltando. Você não percebe até o modelo em produção começar a dar erros. O problema estava no preprocessamento, mas levou dias para diagnosticar.

**Solução**: Testes automatizados capturam regressões imediatamente. Cada função tem casos de teste definidos. Ao modificar código, você roda `pytest` e descobre problemas em segundos, não dias. Mudanças ficam seguras. Refatoração deixa de ser assustadora.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Escrever** testes unitários para funções de carregamento de dados
2. **Utilizar** `pytest.mark.parametrize` para testar múltiplos casos
3. **Testar** cenários de erro (edge cases e exceções)
4. **Configurar** e interpretar relatórios de cobertura de código
5. **Aplicar** padrões AAA (Arrange-Act-Assert) em testes reais
6. **Executar** testes de forma seletiva e eficiente

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Aula 03 - Partes 01 e 02 concluídas
- Estrutura de testes criada
- Pytest instalado e funcionando

**Verificar ambiente:**

```bash
cd c:\Users\diogomiyake\projects\swe4ds-credit-api
.venv\Scripts\activate
pytest --version
```

**Verificar estrutura:**
```
swe4ds-credit-api/
├── pyproject.toml
├── src/
│   ├── __init__.py
│   └── data_loader.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── unit/
        └── __init__.py
```

**Checklist:**
- [ ] Ambiente ativado
- [ ] Pytest disponível
- [ ] Estrutura de testes existe

# 5. Visão geral do que já existe no projeto (continuidade)

Vamos revisar o código que vamos testar. Abra `src/data_loader.py`:

```python
# src/data_loader.py
"""
Módulo para carregamento e preprocessamento de dados de crédito.
"""
from pathlib import Path
from typing import Tuple, List
import pandas as pd


def load_credit_data(
    filepath: Path | None = None,
    use_cache: bool = True
) -> pd.DataFrame:
    """
    Carrega dados de crédito de arquivo CSV ou cache.
    
    Args:
        filepath: Caminho para arquivo CSV. Se None, usa padrão.
        use_cache: Se True, tenta carregar de cache parquet.
        
    Returns:
        DataFrame com dados de crédito.
        
    Raises:
        FileNotFoundError: Se arquivo não existe.
        ValueError: Se dados estão vazios.
    """
    if filepath is None:
        filepath = Path("data/raw/UCI_Credit_Card.csv")
    
    cache_path = Path("data/processed/credit_cache.parquet")
    
    if use_cache and cache_path.exists():
        return pd.read_parquet(cache_path)
    
    if not filepath.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
    
    df = pd.read_csv(filepath)
    
    if df.empty:
        raise ValueError("Dataset está vazio")
    
    if use_cache:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(cache_path)
    
    return df


def preprocess_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Preprocessa dados separando features e target.
    
    Args:
        df: DataFrame com dados brutos.
        
    Returns:
        Tupla (features DataFrame, target Series).
        
    Raises:
        KeyError: Se coluna target não existe.
    """
    target_col = "default payment next month"
    
    if target_col not in df.columns:
        raise KeyError(f"Coluna target '{target_col}' não encontrada")
    
    # Remover ID e target das features
    feature_cols = [c for c in df.columns if c not in ["ID", target_col]]
    
    X = df[feature_cols]
    y = df[target_col]
    
    return X, y


def get_feature_names(df: pd.DataFrame) -> List[str]:
    """
    Retorna lista de nomes de features (exclui ID e target).
    
    Args:
        df: DataFrame com dados.
        
    Returns:
        Lista de nomes de colunas.
    """
    exclude = ["ID", "default payment next month"]
    return [c for c in df.columns if c not in exclude]
```

**O que vamos testar:**
- `load_credit_data`: Carregamento, cache, erros
- `preprocess_data`: Separação features/target, erros
- `get_feature_names`: Filtragem de colunas

# 6. Passo a passo (comandos + código)

## Passo 1: Primeiro Teste Real - get_feature_names

**Intenção**: Começar pelo mais simples para ganhar confiança.

A função `get_feature_names` é a mais simples. Vamos testá-la primeiro.

Crie o arquivo `tests/unit/test_data_loader.py`:

```python
# tests/unit/test_data_loader.py
"""
Testes unitários para o módulo data_loader.

Estes testes verificam o comportamento das funções de
carregamento e preprocessamento de dados de crédito.
"""
import pytest
import pandas as pd
from src.data_loader import get_feature_names


class TestGetFeatureNames:
    """Testes para a função get_feature_names."""
    
    def test_returns_list(self, sample_credit_data):
        """
        Verifica que o retorno é uma lista.
        
        Args:
            sample_credit_data: Fixture do conftest.py
        """
        # ACT
        result = get_feature_names(sample_credit_data)
        
        # ASSERT
        assert isinstance(result, list)
    
    def test_excludes_id_column(self, sample_credit_data):
        """Verifica que coluna ID é excluída."""
        result = get_feature_names(sample_credit_data)
        assert "ID" not in result
    
    def test_excludes_target_column(self, sample_credit_data):
        """Verifica que coluna target é excluída."""
        result = get_feature_names(sample_credit_data)
        assert "default payment next month" not in result
    
    def test_returns_correct_count(self, sample_credit_data):
        """
        Verifica quantidade de features.
        
        23 colunas totais - ID - target = 21 features
        """
        result = get_feature_names(sample_credit_data)
        # Total de colunas (25) - ID - target = 23
        # Nosso fixture tem 25 colunas
        assert len(result) == 23
    
    def test_with_empty_dataframe(self, empty_dataframe):
        """Verifica comportamento com DataFrame vazio."""
        result = get_feature_names(empty_dataframe)
        assert result == []
```

**Rodar o teste:**

```bash
pytest tests/unit/test_data_loader.py -v
```

**Saída esperada:**
```
tests/unit/test_data_loader.py::TestGetFeatureNames::test_returns_list PASSED
tests/unit/test_data_loader.py::TestGetFeatureNames::test_excludes_id_column PASSED
tests/unit/test_data_loader.py::TestGetFeatureNames::test_excludes_target_column PASSED
tests/unit/test_data_loader.py::TestGetFeatureNames::test_returns_correct_count PASSED
tests/unit/test_data_loader.py::TestGetFeatureNames::test_with_empty_dataframe PASSED
```

**CHECKPOINT**: 5 testes passando para `get_feature_names`.

---

## Passo 2: Testando preprocess_data

**Intenção**: Testar função com mais lógica e potencial de erros.

Continue editando `tests/unit/test_data_loader.py`:

```python
# Adicionar ao final do arquivo
from src.data_loader import preprocess_data


class TestPreprocessData:
    """Testes para a função preprocess_data."""
    
    def test_returns_tuple(self, sample_credit_data):
        """Verifica que retorna tupla (X, y)."""
        result = preprocess_data(sample_credit_data)
        assert isinstance(result, tuple)
        assert len(result) == 2
    
    def test_features_is_dataframe(self, sample_credit_data):
        """Verifica que features é DataFrame."""
        X, _ = preprocess_data(sample_credit_data)
        assert isinstance(X, pd.DataFrame)
    
    def test_target_is_series(self, sample_credit_data):
        """Verifica que target é Series."""
        _, y = preprocess_data(sample_credit_data)
        assert isinstance(y, pd.Series)
    
    def test_features_excludes_id(self, sample_credit_data):
        """Verifica que features não contém ID."""
        X, _ = preprocess_data(sample_credit_data)
        assert "ID" not in X.columns
    
    def test_features_excludes_target(self, sample_credit_data):
        """Verifica que features não contém target."""
        X, _ = preprocess_data(sample_credit_data)
        assert "default payment next month" not in X.columns
    
    def test_target_has_correct_values(self, sample_credit_data):
        """Verifica valores do target."""
        _, y = preprocess_data(sample_credit_data)
        # Target deve conter apenas 0 e 1
        assert set(y.unique()).issubset({0, 1})
    
    def test_same_number_of_rows(self, sample_credit_data):
        """Verifica que X e y têm mesmo número de linhas."""
        X, y = preprocess_data(sample_credit_data)
        assert len(X) == len(y) == len(sample_credit_data)
    
    def test_raises_keyerror_without_target(self):
        """Verifica que levanta KeyError se target não existe."""
        df_without_target = pd.DataFrame({
            "col1": [1, 2, 3],
            "col2": [4, 5, 6]
        })
        
        with pytest.raises(KeyError) as exc_info:
            preprocess_data(df_without_target)
        
        assert "default payment next month" in str(exc_info.value)
```

**Rodar testes da classe:**

```bash
pytest tests/unit/test_data_loader.py::TestPreprocessData -v
```

**Esperado**: Todos os 8 testes passam.

**CHECKPOINT**: Função `preprocess_data` testada com cenários de sucesso e erro.

---

## Passo 3: Pytest Parametrize - Múltiplos Casos em Um Teste

**Intenção**: Aprender a testar variações sem repetir código.

O decorator `@pytest.mark.parametrize` permite rodar o mesmo teste com diferentes inputs.

Adicione ao `tests/unit/test_data_loader.py`:

```python
# Adicionar após as classes existentes

class TestGetFeatureNamesParametrized:
    """Demonstração de pytest.mark.parametrize."""
    
    @pytest.mark.parametrize("column_to_check,should_be_included", [
        ("LIMIT_BAL", True),
        ("AGE", True),
        ("SEX", True),
        ("PAY_0", True),
        ("BILL_AMT1", True),
        ("ID", False),
        ("default payment next month", False),
    ])
    def test_column_inclusion(
        self,
        sample_credit_data,
        column_to_check,
        should_be_included
    ):
        """
        Testa se colunas específicas estão ou não incluídas.
        
        Args:
            sample_credit_data: Fixture com dados de exemplo.
            column_to_check: Nome da coluna a verificar.
            should_be_included: Se deve estar na lista de features.
        """
        result = get_feature_names(sample_credit_data)
        
        if should_be_included:
            assert column_to_check in result
        else:
            assert column_to_check not in result
```

**Rodar:**

```bash
pytest tests/unit/test_data_loader.py::TestGetFeatureNamesParametrized -v
```

**Saída:**
```
...::test_column_inclusion[LIMIT_BAL-True] PASSED
...::test_column_inclusion[AGE-True] PASSED
...::test_column_inclusion[SEX-True] PASSED
...::test_column_inclusion[PAY_0-True] PASSED
...::test_column_inclusion[BILL_AMT1-True] PASSED
...::test_column_inclusion[ID-False] PASSED
...::test_column_inclusion[default payment next month-False] PASSED
```

Cada combinação de parâmetros é um teste separado!

**CHECKPOINT**: 7 variações testadas com uma única função de teste.

---

## Passo 4: Testando load_credit_data com Mocks

**Intenção**: Testar função que depende de arquivos sem precisar de arquivos reais.

Adicione ao `tests/unit/test_data_loader.py`:

```python
# Adicionar imports no topo
from pathlib import Path
from unittest.mock import MagicMock
from src.data_loader import load_credit_data


class TestLoadCreditData:
    """Testes para a função load_credit_data."""
    
    def test_loads_from_cache_when_exists(self, mocker, sample_credit_data):
        """
        Verifica que usa cache quando disponível.
        """
        # ARRANGE
        # Mock read_parquet para retornar nosso fixture
        mock_read_parquet = mocker.patch(
            "src.data_loader.pd.read_parquet",
            return_value=sample_credit_data
        )
        
        # Mock Path.exists para cache existir
        mocker.patch("src.data_loader.Path.exists", return_value=True)
        
        # ACT
        result = load_credit_data(use_cache=True)
        
        # ASSERT
        mock_read_parquet.assert_called_once()
        assert result.equals(sample_credit_data)
    
    def test_loads_from_csv_when_no_cache(
        self,
        mocker,
        sample_credit_data,
        tmp_path
    ):
        """
        Verifica carregamento de CSV quando cache não existe.
        """
        # ARRANGE
        # Criar arquivo CSV temporário
        csv_path = tmp_path / "test_data.csv"
        sample_credit_data.to_csv(csv_path, index=False)
        
        # Mock para cache não existir
        def mock_exists(self):
            return self == csv_path
        
        mocker.patch.object(Path, "exists", mock_exists)
        
        # Mock to_parquet para não tentar salvar
        mocker.patch("pandas.DataFrame.to_parquet")
        
        # ACT
        result = load_credit_data(filepath=csv_path, use_cache=False)
        
        # ASSERT
        assert len(result) == len(sample_credit_data)
    
    def test_raises_filenotfound_for_missing_file(self, mocker):
        """
        Verifica que levanta FileNotFoundError para arquivo inexistente.
        """
        # ARRANGE
        mocker.patch.object(Path, "exists", return_value=False)
        
        # ACT & ASSERT
        with pytest.raises(FileNotFoundError) as exc_info:
            load_credit_data(
                filepath=Path("nao_existe.csv"),
                use_cache=False
            )
        
        assert "nao_existe.csv" in str(exc_info.value)
    
    def test_raises_valueerror_for_empty_csv(self, mocker, tmp_path):
        """
        Verifica que levanta ValueError para CSV vazio.
        """
        # ARRANGE
        # Criar CSV vazio (só header)
        empty_csv = tmp_path / "empty.csv"
        pd.DataFrame(columns=["col1", "col2"]).to_csv(empty_csv, index=False)
        
        # Mock cache não existir
        mocker.patch.object(
            Path,
            "exists",
            lambda self: str(self) == str(empty_csv)
        )
        
        # ACT & ASSERT
        with pytest.raises(ValueError) as exc_info:
            load_credit_data(filepath=empty_csv, use_cache=False)
        
        assert "vazio" in str(exc_info.value)
```

**Rodar:**

```bash
pytest tests/unit/test_data_loader.py::TestLoadCreditData -v
```

**CHECKPOINT**: 4 testes de `load_credit_data` passando.

---

## Passo 5: Medindo Cobertura de Código

**Intenção**: Saber quanto do código está sendo testado.

**Rodar testes com cobertura:**

```bash
pytest tests/unit/test_data_loader.py --cov=src --cov-report=term-missing
```

**Saída esperada:**
```
----------- coverage: platform win32, python 3.12.x -----------
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
src/__init__.py           0      0   100%
src/data_loader.py       35      5    86%   41-45
---------------------------------------------------
TOTAL                    35      5    86%
```

**Gerar relatório HTML:**

```bash
pytest --cov=src --cov-report=html
```

Abra `htmlcov/index.html` no navegador para ver relatório visual.

**Interpretando a Cobertura:**

| Cobertura | Significado |
|-----------|-------------|
| < 60% | Baixa - muitos cenários não testados |
| 60-80% | Média - cobertura aceitável |
| 80-90% | Boa - maioria dos cenários cobertos |
| > 90% | Excelente - cobertura completa |

**CHECKPOINT**: Relatório de cobertura gerado mostrando > 80%.

---

## Passo 6: Rodando Testes Seletivamente

**Intenção**: Aprender comandos úteis para execução de testes.

### Comandos Úteis

```bash
# Rodar todos os testes
pytest

# Rodar com verbose
pytest -v

# Rodar arquivo específico
pytest tests/unit/test_data_loader.py

# Rodar classe específica
pytest tests/unit/test_data_loader.py::TestPreprocessData

# Rodar teste específico
pytest tests/unit/test_data_loader.py::TestGetFeatureNames::test_returns_list

# Rodar testes que falharam na última execução
pytest --lf

# Parar no primeiro erro
pytest -x

# Mostrar prints (útil para debug)
pytest -s

# Rodar em paralelo (precisa pytest-xdist)
# uv pip install pytest-xdist
# pytest -n auto
```

### Usando Markers

Adicione markers aos testes para categorização:

```python
@pytest.mark.slow
def test_something_slow():
    """Teste marcado como lento."""
    pass


@pytest.mark.integration
def test_with_external_service():
    """Teste de integração."""
    pass
```

```bash
# Rodar apenas testes lentos
pytest -m slow

# Rodar excluindo testes lentos
pytest -m "not slow"

# Rodar integração
pytest -m integration
```

**CHECKPOINT**: Você sabe executar testes de forma seletiva.

---

## Passo 7: Arquivo de Testes Completo

**Intenção**: Consolidar todo o código em um arquivo organizado.

O arquivo `tests/unit/test_data_loader.py` completo:

```python
# tests/unit/test_data_loader.py
"""
Testes unitários para o módulo data_loader.

Este módulo contém testes para:
- load_credit_data: Carregamento de dados
- preprocess_data: Preprocessamento
- get_feature_names: Extração de features
"""
import pytest
import pandas as pd
from pathlib import Path
from src.data_loader import (
    load_credit_data,
    preprocess_data,
    get_feature_names,
)


class TestGetFeatureNames:
    """Testes para a função get_feature_names."""
    
    def test_returns_list(self, sample_credit_data):
        """Verifica que o retorno é uma lista."""
        result = get_feature_names(sample_credit_data)
        assert isinstance(result, list)
    
    def test_excludes_id_column(self, sample_credit_data):
        """Verifica que coluna ID é excluída."""
        result = get_feature_names(sample_credit_data)
        assert "ID" not in result
    
    def test_excludes_target_column(self, sample_credit_data):
        """Verifica que coluna target é excluída."""
        result = get_feature_names(sample_credit_data)
        assert "default payment next month" not in result
    
    def test_returns_correct_count(self, sample_credit_data):
        """Verifica quantidade de features (23)."""
        result = get_feature_names(sample_credit_data)
        assert len(result) == 23
    
    def test_with_empty_dataframe(self, empty_dataframe):
        """Verifica comportamento com DataFrame vazio."""
        result = get_feature_names(empty_dataframe)
        assert result == []


class TestGetFeatureNamesParametrized:
    """Testes parametrizados para get_feature_names."""
    
    @pytest.mark.parametrize("column,should_include", [
        ("LIMIT_BAL", True),
        ("AGE", True),
        ("SEX", True),
        ("ID", False),
        ("default payment next month", False),
    ])
    def test_column_inclusion(
        self,
        sample_credit_data,
        column,
        should_include
    ):
        """Testa inclusão/exclusão de colunas específicas."""
        result = get_feature_names(sample_credit_data)
        
        if should_include:
            assert column in result
        else:
            assert column not in result


class TestPreprocessData:
    """Testes para a função preprocess_data."""
    
    def test_returns_tuple(self, sample_credit_data):
        """Verifica que retorna tupla (X, y)."""
        result = preprocess_data(sample_credit_data)
        assert isinstance(result, tuple)
        assert len(result) == 2
    
    def test_features_is_dataframe(self, sample_credit_data):
        """Verifica que features é DataFrame."""
        X, _ = preprocess_data(sample_credit_data)
        assert isinstance(X, pd.DataFrame)
    
    def test_target_is_series(self, sample_credit_data):
        """Verifica que target é Series."""
        _, y = preprocess_data(sample_credit_data)
        assert isinstance(y, pd.Series)
    
    def test_features_excludes_id(self, sample_credit_data):
        """Verifica que features não contém ID."""
        X, _ = preprocess_data(sample_credit_data)
        assert "ID" not in X.columns
    
    def test_features_excludes_target(self, sample_credit_data):
        """Verifica que features não contém target."""
        X, _ = preprocess_data(sample_credit_data)
        assert "default payment next month" not in X.columns
    
    def test_target_has_binary_values(self, sample_credit_data):
        """Verifica que target contém apenas 0 e 1."""
        _, y = preprocess_data(sample_credit_data)
        assert set(y.unique()).issubset({0, 1})
    
    def test_same_number_of_rows(self, sample_credit_data):
        """Verifica que X e y têm mesmo número de linhas."""
        X, y = preprocess_data(sample_credit_data)
        assert len(X) == len(y) == len(sample_credit_data)
    
    def test_raises_keyerror_without_target(self):
        """Verifica KeyError quando target não existe."""
        df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        
        with pytest.raises(KeyError) as exc_info:
            preprocess_data(df)
        
        assert "default payment next month" in str(exc_info.value)


class TestLoadCreditData:
    """Testes para a função load_credit_data."""
    
    def test_loads_from_cache(self, mocker, sample_credit_data):
        """Verifica uso do cache quando disponível."""
        mocker.patch(
            "src.data_loader.pd.read_parquet",
            return_value=sample_credit_data
        )
        mocker.patch("src.data_loader.Path.exists", return_value=True)
        
        result = load_credit_data(use_cache=True)
        
        assert result.equals(sample_credit_data)
    
    def test_raises_filenotfound(self, mocker):
        """Verifica FileNotFoundError para arquivo inexistente."""
        mocker.patch.object(Path, "exists", return_value=False)
        
        with pytest.raises(FileNotFoundError):
            load_credit_data(
                filepath=Path("nao_existe.csv"),
                use_cache=False
            )
    
    def test_raises_valueerror_for_empty(self, mocker, tmp_path):
        """Verifica ValueError para dados vazios."""
        empty_csv = tmp_path / "empty.csv"
        pd.DataFrame(columns=["col"]).to_csv(empty_csv, index=False)
        
        mocker.patch.object(
            Path, "exists",
            lambda self: str(self) == str(empty_csv)
        )
        
        with pytest.raises(ValueError) as exc_info:
            load_credit_data(filepath=empty_csv, use_cache=False)
        
        assert "vazio" in str(exc_info.value)
```

**Rodar todos os testes:**

```bash
pytest tests/unit/test_data_loader.py -v --cov=src
```

**CHECKPOINT**: Todos os testes passando com cobertura > 80%.

---

## Passo 8: Commit Final

**Intenção**: Salvar o trabalho feito.

```bash
# Ver status
git status

# Adicionar arquivos
git add tests/unit/test_data_loader.py

# Commit
git commit -m "test: adiciona testes unitários para data_loader

Testes adicionados:
- TestGetFeatureNames: 5 testes
- TestGetFeatureNamesParametrized: 5 variações
- TestPreprocessData: 8 testes
- TestLoadCreditData: 3 testes

Cobertura: 86% do módulo data_loader"
```

**CHECKPOINT**: Commit realizado com mensagem descritiva.

# 7. Testes rápidos e validação

```bash
# Verificar todos os testes passam
pytest tests/unit/ -v

# Verificar cobertura
pytest --cov=src --cov-report=term-missing

# Verificar nenhum warning
pytest tests/unit/ -W error
```

**Esperado:**
- Todos os testes passando (21+ testes)
- Cobertura acima de 80%
- Sem warnings

# 8. Observabilidade e boas práticas (mini-bloco)

### Padrões Aplicados

1. **Organização por Classe**
   - Uma classe de teste por função/módulo
   - Facilita navegação e manutenção
   - **Trade-off**: Arquivos maiores, mas bem organizados

2. **Nomes Descritivos**
   - `test_raises_keyerror_without_target` é auto-explicativo
   - Docstrings complementam quando necessário
   - **Trade-off**: Nomes longos, mas claros

3. **Fixtures Reutilizáveis**
   - `sample_credit_data` usado em muitos testes
   - Definido uma vez no conftest.py
   - **Trade-off**: Dependência entre testes e fixtures

4. **Parametrize para Variações**
   - Um teste, múltiplos casos
   - Reduz duplicação de código
   - **Trade-off**: Mais complexo de ler

5. **Testar Erros Explicitamente**
   - `pytest.raises` para exceções
   - Verifica mensagem de erro
   - **Trade-off**: Testes acoplados à implementação de erro

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| `ModuleNotFoundError: src` | Pythonpath não configurado | Adicione `pythonpath = ["."]` em pyproject.toml |
| `fixture 'sample_credit_data' not found` | conftest.py não encontrado | Verifique que está em tests/ |
| Teste não descoberto | Nome não começa com test_ | Renomeie função/arquivo |
| Mock não funciona | Caminho de patch errado | Patch onde é usado, não onde definido |
| `AssertionError` em parametrize | Parâmetros incorretos | Verifique ordem e tipos |
| Cobertura 0% | source errado | Verifique `[tool.coverage.run]` |

# 10. Exercícios (básico e avançado)

## Exercício Básico 1: Adicionar Teste de Edge Case

Adicione um teste que verifica o comportamento de `get_feature_names` quando o DataFrame tem apenas as colunas ID e target:

```python
def test_returns_empty_when_only_metadata(self):
    """Quando só há ID e target, retorna lista vazia."""
    df = pd.DataFrame({
        "ID": [1, 2],
        "default payment next month": [0, 1]
    })
    result = get_feature_names(df)
    assert result == []
```

**Critério**: Teste passa.

## Exercício Básico 2: Teste Parametrizado

Crie teste parametrizado para verificar tipos de dados das colunas após `preprocess_data`:

```python
@pytest.mark.parametrize("col,expected_dtype", [
    ("LIMIT_BAL", "int64"),
    ("AGE", "int64"),
    ("PAY_0", "int64"),
])
def test_feature_dtypes(self, sample_credit_data, col, expected_dtype):
    # Implemente
    pass
```

**Critério**: 3 casos de teste passando.

## Exercício Avançado: 100% de Cobertura

Analise o relatório de cobertura e adicione testes para cobrir as linhas faltantes. Objetive 100% de cobertura no `data_loader.py`.

**Dica**: Provavelmente falta testar o caminho onde cache é salvo (mkdir + to_parquet).

**Critério**: `pytest --cov=src` mostra 100% para data_loader.py.

# 11. Resultados e Lições

## Métricas Finais

| Métrica | Valor |
|---------|-------|
| Testes escritos | 21+ |
| Classes de teste | 4 |
| Cobertura | > 80% |
| Tempo de execução | < 2s |

## Lições Aprendidas

1. **Comece pelo simples** - `get_feature_names` antes de `load_credit_data`
2. **Parametrize economiza código** - Uma função, muitos casos
3. **Mocks isolam dependências** - Não precisa de arquivos reais
4. **Cobertura guia** - Mostra o que falta testar
5. **Testes são documentação** - Mostram como usar o código

## Comandos Essenciais

```bash
# Rodar testes
pytest tests/unit/ -v

# Com cobertura
pytest --cov=src --cov-report=html

# Apenas falhas anteriores
pytest --lf

# Parar no primeiro erro
pytest -x
```

# 12. Encerramento e gancho para a próxima aula (script)

Excelente trabalho! Você acabou de escrever mais de 20 testes para código real de Data Science. Testou funções de carregamento de dados, preprocessamento, e extração de features. Usou fixtures, mocks, parametrize, e mediu cobertura.

Esse é o tipo de skill que diferencia um cientista de dados que "faz código funcionar" de um profissional que entrega código confiável.

Na próxima aula, vamos fechar o ciclo. Vamos configurar GitHub Actions para rodar esses testes automaticamente a cada push. Você vai ver como criar um pipeline de CI que bloqueia código quebrado de entrar no repositório. Vamos também fazer um exercício completo de TDD, criando uma nova função do zero usando Red → Green → Refactor.

Prepare-se para integração contínua! Até lá.
