"""
Módulo de pré-processamento de dados para benchmarking de latência em ML.

Caso de uso da Aula 01: **detecção de fraude bancária em tempo real**.
Cada linha representa uma transação de cartão e o objetivo é sinalizar
fraudes (target=1) com a menor latência possível, pois um atraso na
detecção implica perda financeira direta para o banco.

Implementa o pipeline de pré-processamento conforme discutido na seção
'Fundamentação Teórica' da aula, onde a latência de pré-processamento
(L_pre) é um dos componentes da latência total do sistema.

Referência:
    Sculley, D. et al. (2015). Hidden Technical Debt in Machine Learning
    Systems. NeurIPS '15.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# Nomes de features alinhados ao caso de uso de detecção de fraude.
# Os valores são gerados sinteticamente por make_classification, mas os
# nomes representam sinais reais usados em sistemas antifraude (Bahnsen
# et al., 2016; Carcillo et al., 2018).
FRAUD_FEATURE_NAMES: list[str] = [
    "tx_amount_z",            # valor da transação (z-score)
    "amount_to_avg_ratio",    # razão entre valor atual e média do cliente
    "hour_sin",               # hora do dia (componente sazonal)
    "hour_cos",               # hora do dia (componente sazonal)
    "time_since_last_tx_s",   # segundos desde a última transação
    "distance_from_home_km",  # distância geográfica do endereço cadastrado
    "distance_from_last_tx_km",  # distância da transação anterior
    "merchant_risk_score",    # score de risco do estabelecimento
    "mcc_risk_score",         # score de risco da categoria do comércio
    "velocity_1h",            # nº de transações na última hora
    "velocity_24h",           # nº de transações nas últimas 24h
    "avg_amount_30d",         # ticket médio nos últimos 30 dias
    "card_age_days",          # tempo de uso do cartão
    "cross_border_score",     # indicador de operação internacional
    "device_anomaly_score",   # anomalia do dispositivo/IP usado
]


class DataPreprocessor:
    """
    Pipeline de pré-processamento com medição de latência em cada etapa.

    Implementa o conceito de decomposição da latência total em componentes
    individuais (L_pre, L_inferencia, L_pos), conforme Crankshaw et al. (2017),
    permitindo identificar gargalos no pipeline de ML.

    Referência:
        Crankshaw, D. et al. (2017). Clipper: A Low-Latency Online Prediction
        Serving System. NSDI '17.

    Attributes:
        scaler: StandardScaler para normalização de features.
        feature_names: Nomes das colunas de features.
        latency_log: Registro de latência de cada operação.
    """

    def __init__(self, random_state: int = 42) -> None:
        """
        Inicializa o pré-processador.

        Args:
            random_state: Seed para reprodutibilidade.
        """
        self.scaler = StandardScaler()
        self.feature_names: list[str] = []
        self.latency_log: list[dict[str, float]] = []
        self.random_state = random_state

    # ------------------------------------------------------------------
    # Geração de dataset sintético
    # ------------------------------------------------------------------
    @staticmethod
    def generate_synthetic_dataset(
        output_path: str = "data/raw/dataset.csv",
        n_samples: int = 10_000,
        n_features: int = 15,
        n_informative: int = 10,
        n_redundant: int = 2,
        random_state: int = 42,
        fraud_rate: float = 0.05,
    ) -> pd.DataFrame:
        """
        Gera dataset sintético de **transações bancárias** para benchmarking.

        Simula um stream de transações de cartão onde a classe positiva
        (target=1) representa fraude. As features são geradas com
        ``sklearn.datasets.make_classification`` e renomeadas com termos
        do domínio antifraude (valor, distância, velocidade, score de
        risco do estabelecimento, etc.).

        O desbalanceamento (default ~5% de fraudes) reflete o cenário
        real, onde a maioria das transações é legítima e a minoria
        precisa ser sinalizada com latência mínima.

        Args:
            output_path: Caminho para salvar o CSV.
            n_samples: Número de transações.
            n_features: Número total de features.
            n_informative: Número de features informativas.
            n_redundant: Número de features redundantes.
            random_state: Seed para reprodutibilidade.
            fraud_rate: Proporção esperada de fraudes (classe 1).

        Returns:
            DataFrame com o dataset gerado.
        """
        legit_rate = 1.0 - fraud_rate
        X, y = make_classification(
            n_samples=n_samples,
            n_features=n_features,
            n_informative=n_informative,
            n_redundant=n_redundant,
            n_clusters_per_class=2,
            weights=[legit_rate, fraud_rate],
            flip_y=0.01,
            random_state=random_state,
        )

        if n_features == len(FRAUD_FEATURE_NAMES):
            feature_cols = list(FRAUD_FEATURE_NAMES)
        else:
            feature_cols = [f"feature_{i}" for i in range(n_features)]
        df = pd.DataFrame(X, columns=feature_cols)
        df["target"] = y

        # Garantir que o diretório existe
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)

        return df

    # ------------------------------------------------------------------
    # Pipeline de pré-processamento
    # ------------------------------------------------------------------
    def load_data(self, filepath: str) -> pd.DataFrame:
        """
        Carrega dados de um arquivo CSV com medição de latência.

        Mede o tempo de I/O, que é parte da latência de pré-processamento
        (L_pre). Em produção, leituras de disco podem ser gargalos
        significativos conforme Sculley et al. (2015).

        Args:
            filepath: Caminho do arquivo CSV.

        Returns:
            DataFrame com os dados carregados.

        Raises:
            FileNotFoundError: Se o arquivo não existir.
        """
        start = time.perf_counter()
        df = pd.read_csv(filepath)
        elapsed = time.perf_counter() - start

        self.feature_names = [c for c in df.columns if c != "target"]
        self._log_latency("load_data", elapsed)
        return df

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpa dados removendo duplicatas e tratando valores ausentes.

        Implementa etapas de limpeza que contribuem para a latência de
        pré-processamento. A medição granular permite identificar se a
        limpeza é um gargalo no pipeline.

        Args:
            df: DataFrame de entrada.

        Returns:
            DataFrame limpo.
        """
        start = time.perf_counter()

        # Remover duplicatas
        df_clean = df.drop_duplicates()

        # Preencher valores ausentes com a mediana (robusto a outliers)
        for col in self.feature_names:
            if df_clean[col].isna().any():
                df_clean[col] = df_clean[col].fillna(df_clean[col].median())

        elapsed = time.perf_counter() - start
        self._log_latency("clean_data", elapsed)
        return df_clean

    def prepare_features(
        self, df: pd.DataFrame, fit: bool = True
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Prepara features aplicando normalização (StandardScaler).

        A normalização é parte da latência de pré-processamento. O StandardScaler
        realiza a transformação z = (x - μ) / σ com complexidade O(n·d),
        onde n = amostras e d = features.

        Args:
            df: DataFrame com features e target.
            fit: Se True, ajusta o scaler; se False, apenas transforma.

        Returns:
            Tupla (X, y) com features normalizadas e target.
        """
        start = time.perf_counter()

        X = df[self.feature_names].values
        y = df["target"].values

        if fit:
            X = self.scaler.fit_transform(X)
        else:
            X = self.scaler.transform(X)

        elapsed = time.perf_counter() - start
        self._log_latency("prepare_features", elapsed)
        return X, y

    def split_data(
        self,
        X: np.ndarray,
        y: np.ndarray,
        test_size: float = 0.2,
        val_size: float = 0.1,
    ) -> dict[str, np.ndarray]:
        """
        Divide dados em treino, validação e teste.

        Conforme boas práticas de benchmarking (Reddi et al., 2020), a
        separação de dados deve ser feita antes de qualquer otimização
        para garantir avaliação justa.

        Args:
            X: Features.
            y: Target.
            test_size: Proporção do conjunto de teste.
            val_size: Proporção do conjunto de validação (relativa ao treino).

        Returns:
            Dicionário com splits X_train, X_val, X_test, y_train, y_val, y_test.
        """
        start = time.perf_counter()

        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state, stratify=y
        )

        # val_size relativo ao conjunto temporário
        relative_val = val_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp,
            y_temp,
            test_size=relative_val,
            random_state=self.random_state,
            stratify=y_temp,
        )

        elapsed = time.perf_counter() - start
        self._log_latency("split_data", elapsed)

        return {
            "X_train": X_train,
            "X_val": X_val,
            "X_test": X_test,
            "y_train": y_train,
            "y_val": y_val,
            "y_test": y_test,
        }

    def get_latency_report(self) -> pd.DataFrame:
        """
        Retorna relatório de latência de todas as operações registradas.

        Implementa o conceito de decomposição de latência onde
        L_total = Σ L_etapa, permitindo identificar gargalos
        conforme Crankshaw et al. (2017).

        Returns:
            DataFrame com operação, latência (ms) e percentual do total.
        """
        if not self.latency_log:
            return pd.DataFrame(columns=["operation", "latency_ms", "pct_total"])

        df = pd.DataFrame(self.latency_log)
        total = df["latency_ms"].sum()
        df["pct_total"] = (df["latency_ms"] / total * 100).round(2)
        return df

    # ------------------------------------------------------------------
    # Helpers privados
    # ------------------------------------------------------------------
    def _log_latency(self, operation: str, elapsed_seconds: float) -> None:
        """Registra latência de uma operação em milissegundos."""
        self.latency_log.append(
            {"operation": operation, "latency_ms": round(elapsed_seconds * 1000, 4)}
        )
