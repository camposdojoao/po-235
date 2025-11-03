"""Testes unitários para o módulo de inferências."""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.ensemble import RandomForestClassifier

from models.inferences import Inferences


def test_load_model(trained_model_path: Path) -> None:
    """
    Testa o carregamento de um modelo treinado a partir de arquivo.

    Verifica se o modelo é carregado corretamente do arquivo .joblib
    e se é atribuído corretamente ao atributo da instância.

    Args:
        trained_model_path: Caminho para o arquivo de modelo treinado (fixture).

    Asserts:
        - O modelo carregado não é None
        - O atributo modelo da instância não é None
        - O modelo carregado é uma instância de RandomForestClassifier
    """
    inference = Inferences()
    loaded_model = inference.load_model(str(trained_model_path))

    assert loaded_model is not None
    assert inference.modelo is not None
    assert isinstance(inference.modelo, RandomForestClassifier)


def test_load_model_arquivo_inexistente() -> None:
    """
    Testa o comportamento ao tentar carregar modelo de arquivo inexistente.

    Verifica se FileNotFoundError é lançado quando tentamos carregar
    um modelo de um caminho que não existe.

    Raises:
        FileNotFoundError: Quando o arquivo especificado não existe.
    """
    inference = Inferences()

    with pytest.raises(FileNotFoundError):
        inference.load_model("caminho/inexistente/modelo.joblib")


def test_model_predict(sample_features: pd.DataFrame, trained_model_path: Path) -> None:
    """
    Testa a realização de predições com dados válidos.

    Verifica se o modelo consegue fazer predições após ser carregado
    e se retorna um array numpy com o tamanho correto.

    Args:
        sample_features: DataFrame com features de exemplo (fixture).
        trained_model_path: Caminho para o arquivo de modelo treinado (fixture).

    Asserts:
        - As predições não são None
        - As predições são um array numpy
        - O número de predições corresponde ao número de amostras de entrada
    """
    inference = Inferences()
    inference.load_model(str(trained_model_path))
    predictions = inference.model_predict(sample_features)

    assert predictions is not None
    assert isinstance(predictions, np.ndarray)
    assert len(predictions) == len(sample_features)


def test_model_predict_sem_modelo() -> None:
    """
    Testa o comportamento ao tentar fazer predição sem carregar modelo.

    Verifica se ValueError é lançado com mensagem apropriada quando
    tentamos fazer predições sem ter carregado um modelo previamente.

    Raises:
        ValueError: Quando o modelo não foi carregado antes da predição.

    Asserts:
        - A mensagem de erro contém "não foi carregado"
    """
    inference = Inferences()

    with pytest.raises(ValueError) as exc_info:
        inference.model_predict(pd.DataFrame({"col1": [1, 2, 3]}))

    assert "não foi carregado" in str(exc_info.value)


def test_model_predict_valores_validos(
    sample_features: pd.DataFrame, trained_model_path: Path
) -> None:
    """
    Testa se as predições retornam apenas valores válidos de classificação.

    Verifica se todas as predições do modelo estão dentro do conjunto
    esperado de classes {0, 1, 2}, que representam as categorias de
    qualidade do vinho (Ruim, Média, Boa).

    Args:
        sample_features: DataFrame com features de exemplo (fixture).
        trained_model_path: Caminho para o arquivo de modelo treinado (fixture).

    Asserts:
        - Todas as predições pertencem ao conjunto {0, 1, 2}

    Raises:
        AssertionError: Se houver predições fora do conjunto válido.
    """
    inference = Inferences()
    inference.load_model(str(trained_model_path))
    predictions = inference.model_predict(sample_features)

    unique_predictions = set(predictions)
    assert unique_predictions.issubset({0, 1, 2}), (
        f"Predições devem ser 0, 1 ou 2, mas obteve: {unique_predictions}"
    )
