"""
Módulo de utilitários para serialização, configuração e logging.

Fornece funções auxiliares para salvar/carregar modelos, registrar
métricas e gerenciar configurações do pipeline de ML.

Referência:
    Sculley, D. et al. (2015). Hidden Technical Debt in Machine Learning
    Systems. NeurIPS '15.
"""

from __future__ import annotations

import json
import pickle
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


def save_model(model: Any, filepath: str) -> None:
    """
    Serializa modelo treinado em disco.

    Conforme Sculley et al. (2015), a serialização de modelos é um componente
    crítico do pipeline de ML que impacta a latência de carregamento em produção.

    Args:
        model: Modelo treinado (qualquer objeto pickle-serializável).
        filepath: Caminho para salvar o modelo (.pkl).
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(model, f)


def load_model(filepath: str) -> Any:
    """
    Carrega modelo serializado do disco.

    A latência de carregamento é parte do cold-start de sistemas de serving,
    conforme Crankshaw et al. (2017).

    Args:
        filepath: Caminho do modelo serializado (.pkl).

    Returns:
        Modelo deserializado.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Modelo não encontrado: {filepath}")
    with open(path, "rb") as f:
        return pickle.load(f)


def save_metrics(metrics: dict[str, Any], filepath: str) -> None:
    """
    Salva métricas em formato JSON.

    Args:
        metrics: Dicionário de métricas.
        filepath: Caminho para salvar (.json).
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Converter tipos numpy para nativos Python
    serializable = _make_json_serializable(metrics)
    serializable["_saved_at"] = datetime.now(timezone.utc).isoformat()

    with open(path, "w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2, ensure_ascii=False)


def load_metrics(filepath: str) -> dict[str, Any]:
    """
    Carrega métricas de arquivo JSON.

    Args:
        filepath: Caminho do arquivo de métricas (.json).

    Returns:
        Dicionário de métricas.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo de métricas não encontrado: {filepath}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_config(filepath: str) -> dict[str, Any]:
    """
    Carrega configuração de arquivo JSON.

    Args:
        filepath: Caminho do arquivo de configuração (.json).

    Returns:
        Dicionário de configuração.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Configuração não encontrada: {filepath}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_dataframe(df: pd.DataFrame, filepath: str) -> None:
    """
    Salva DataFrame em CSV.

    Args:
        df: DataFrame a salvar.
        filepath: Caminho para salvar (.csv).
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def setup_output_dirs(base_path: str = ".") -> dict[str, Path]:
    """
    Cria diretórios de output se não existirem.

    Args:
        base_path: Caminho base da aula.

    Returns:
        Dicionário com paths dos diretórios criados.
    """
    dirs = {
        "models": Path(base_path) / "outputs" / "models",
        "figures": Path(base_path) / "outputs" / "figures",
        "logs": Path(base_path) / "outputs" / "logs",
        "processed": Path(base_path) / "data" / "processed",
    }
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)
    return dirs


def format_latency_table(results: list[dict[str, Any]]) -> pd.DataFrame:
    """
    Formata resultados de benchmark em tabela legível.

    Args:
        results: Lista de dicionários de benchmark.

    Returns:
        DataFrame formatado com métricas de latência.
    """
    df = pd.DataFrame(results)
    # Arredondar colunas numéricas
    float_cols = df.select_dtypes(include=[np.floating]).columns
    df[float_cols] = df[float_cols].round(4)
    return df


# ------------------------------------------------------------------
# Helpers privados
# ------------------------------------------------------------------


def _make_json_serializable(obj: Any) -> Any:
    """Converte tipos numpy para tipos nativos Python."""
    if isinstance(obj, dict):
        return {k: _make_json_serializable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_make_json_serializable(item) for item in obj]
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj
