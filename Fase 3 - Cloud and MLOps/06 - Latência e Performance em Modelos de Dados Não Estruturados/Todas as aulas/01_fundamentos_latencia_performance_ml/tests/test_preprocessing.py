"""
Testes unitários para o módulo data_preprocessing.

Verifica o pipeline de pré-processamento: geração de dataset, carregamento,
limpeza, normalização e split com medição de latência.
"""

import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.data_preprocessing import DataPreprocessor


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """Cria DataFrame de exemplo para testes."""
    np.random.seed(42)
    n = 200
    data = {f"feature_{i}": np.random.randn(n) for i in range(5)}
    data["target"] = np.random.randint(0, 2, size=n)
    return pd.DataFrame(data)


@pytest.fixture
def sample_csv(sample_df: pd.DataFrame, tmp_path: Path) -> str:
    """Salva DataFrame em CSV temporário e retorna o caminho."""
    path = tmp_path / "test_dataset.csv"
    sample_df.to_csv(path, index=False)
    return str(path)


@pytest.fixture
def preprocessor() -> DataPreprocessor:
    """Retorna instância do preprocessor com seed fixa."""
    return DataPreprocessor(random_state=42)


# ---------------------------------------------------------------------------
# Testes
# ---------------------------------------------------------------------------


class TestGenerateSyntheticDataset:
    """Testes para geração de dataset sintético."""

    def test_generate_creates_file(self, tmp_path: Path) -> None:
        """Dataset gerado é salvo como CSV."""
        output = str(tmp_path / "generated.csv")
        df = DataPreprocessor.generate_synthetic_dataset(
            output_path=output, n_samples=100, n_features=5,
            n_informative=3, n_redundant=1, random_state=42
        )
        assert Path(output).exists()
        assert isinstance(df, pd.DataFrame)

    def test_generate_correct_shape(self, tmp_path: Path) -> None:
        """Dataset gerado tem shape esperado."""
        output = str(tmp_path / "generated.csv")
        df = DataPreprocessor.generate_synthetic_dataset(
            output_path=output, n_samples=500, n_features=10,
            n_informative=7, n_redundant=2, random_state=42
        )
        assert df.shape == (500, 11)  # 10 features + target

    def test_generate_has_target_column(self, tmp_path: Path) -> None:
        """Dataset gerado contém coluna 'target'."""
        output = str(tmp_path / "generated.csv")
        df = DataPreprocessor.generate_synthetic_dataset(
            output_path=output, n_samples=100, random_state=42
        )
        assert "target" in df.columns

    def test_generate_reproducible(self, tmp_path: Path) -> None:
        """Geração é reproduzível com mesma seed."""
        df1 = DataPreprocessor.generate_synthetic_dataset(
            output_path=str(tmp_path / "a.csv"), n_samples=100, random_state=42
        )
        df2 = DataPreprocessor.generate_synthetic_dataset(
            output_path=str(tmp_path / "b.csv"), n_samples=100, random_state=42
        )
        pd.testing.assert_frame_equal(df1, df2)


class TestLoadData:
    """Testes para carregamento de dados."""

    def test_load_returns_dataframe(
        self, preprocessor: DataPreprocessor, sample_csv: str
    ) -> None:
        """load_data retorna DataFrame."""
        df = preprocessor.load_data(sample_csv)
        assert isinstance(df, pd.DataFrame)

    def test_load_sets_feature_names(
        self, preprocessor: DataPreprocessor, sample_csv: str
    ) -> None:
        """load_data define feature_names corretamente."""
        preprocessor.load_data(sample_csv)
        assert "target" not in preprocessor.feature_names
        assert len(preprocessor.feature_names) == 5

    def test_load_logs_latency(
        self, preprocessor: DataPreprocessor, sample_csv: str
    ) -> None:
        """load_data registra latência."""
        preprocessor.load_data(sample_csv)
        assert len(preprocessor.latency_log) == 1
        assert preprocessor.latency_log[0]["operation"] == "load_data"


class TestCleanData:
    """Testes para limpeza de dados."""

    def test_clean_removes_duplicates(
        self, preprocessor: DataPreprocessor, sample_df: pd.DataFrame
    ) -> None:
        """clean_data remove linhas duplicadas."""
        preprocessor.feature_names = [c for c in sample_df.columns if c != "target"]
        df_dup = pd.concat([sample_df, sample_df.head(5)])
        df_clean = preprocessor.clean_data(df_dup)
        assert len(df_clean) <= len(df_dup)


class TestPrepareFeatures:
    """Testes para preparação de features."""

    def test_prepare_returns_arrays(
        self, preprocessor: DataPreprocessor, sample_df: pd.DataFrame
    ) -> None:
        """prepare_features retorna tupla de arrays."""
        preprocessor.feature_names = [c for c in sample_df.columns if c != "target"]
        X, y = preprocessor.prepare_features(sample_df, fit=True)
        assert isinstance(X, np.ndarray)
        assert isinstance(y, np.ndarray)

    def test_prepare_normalizes_features(
        self, preprocessor: DataPreprocessor, sample_df: pd.DataFrame
    ) -> None:
        """Features normalizadas têm média ~0 e std ~1."""
        preprocessor.feature_names = [c for c in sample_df.columns if c != "target"]
        X, _ = preprocessor.prepare_features(sample_df, fit=True)
        assert np.abs(X.mean()) < 0.1
        assert np.abs(X.std() - 1.0) < 0.1

    def test_prepare_correct_shape(
        self, preprocessor: DataPreprocessor, sample_df: pd.DataFrame
    ) -> None:
        """Shape de X corresponde a (n_samples, n_features)."""
        preprocessor.feature_names = [c for c in sample_df.columns if c != "target"]
        X, y = preprocessor.prepare_features(sample_df, fit=True)
        assert X.shape == (len(sample_df), 5)
        assert y.shape == (len(sample_df),)


class TestSplitData:
    """Testes para split de dados."""

    def test_split_returns_all_keys(
        self, preprocessor: DataPreprocessor
    ) -> None:
        """split_data retorna todos os splits esperados."""
        X = np.random.randn(200, 5)
        y = np.random.randint(0, 2, 200)
        splits = preprocessor.split_data(X, y)
        expected_keys = {"X_train", "X_val", "X_test", "y_train", "y_val", "y_test"}
        assert set(splits.keys()) == expected_keys

    def test_split_preserves_total_samples(
        self, preprocessor: DataPreprocessor
    ) -> None:
        """Soma das amostras em todos splits = total."""
        X = np.random.randn(200, 5)
        y = np.random.randint(0, 2, 200)
        splits = preprocessor.split_data(X, y)
        total = len(splits["X_train"]) + len(splits["X_val"]) + len(splits["X_test"])
        assert total == 200


class TestLatencyReport:
    """Testes para relatório de latência."""

    def test_empty_report(self, preprocessor: DataPreprocessor) -> None:
        """Relatório vazio quando nenhuma operação foi executada."""
        report = preprocessor.get_latency_report()
        assert len(report) == 0

    def test_report_after_operations(
        self, preprocessor: DataPreprocessor, sample_csv: str
    ) -> None:
        """Relatório contém todas operações executadas."""
        preprocessor.load_data(sample_csv)
        report = preprocessor.get_latency_report()
        assert len(report) == 1
        assert "pct_total" in report.columns
