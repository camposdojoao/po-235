"""Testes unitários para o módulo de treinamento de modelos."""

import pandas as pd
import pytest
from sklearn.ensemble import RandomForestClassifier

from models.model import Modelo


def test_init_modelo_random_forest() -> None:
    """
    Testa a inicialização do modelo Random Forest.

    Verifica se o modelo Random Forest é corretamente instanciado
    com os parâmetros adequados, incluindo random_state
    para reprodutibilidade.

    Asserts:
        - O modelo é uma instância de RandomForestClassifier
        - O random_state está configurado como 42
    """
    modelo = Modelo()
    assert isinstance(modelo.modelo, RandomForestClassifier)
    assert modelo.modelo.random_state == 42


def test_apply_model_sem_dados() -> None:
    """
    Testa o comportamento ao tentar treinar sem dados preparados.

    Verifica se ValueError é lançado com mensagem apropriada quando
    tentamos treinar um modelo sem ter preparado os dados de treino
    (X_train e y_train) previamente.

    Raises:
        ValueError: Quando os dados de treino não foram preparados.

    Asserts:
        - A mensagem de erro contém "não foram preparados"
    """
    modelo = Modelo()

    with pytest.raises(ValueError) as exc_info:
        modelo.apply_model()

    assert "não foram preparados" in str(exc_info.value)


def test_apply_model_com_dados(
    prepared_train_data: tuple[pd.DataFrame, pd.Series],
) -> None:
    """
    Testa o treinamento do modelo com dados válidos.

    Verifica se o modelo é treinado com sucesso quando dados válidos
    (X_train e y_train) são fornecidos, e se o modelo resultante
    possui a capacidade de fazer predições.

    Args:
        prepared_train_data: Tupla com (X, y) preparados (fixture).

    Asserts:
        - O modelo treinado não é None
        - O modelo possui o método predict
    """
    X, y = prepared_train_data  # noqa: N806
    modelo = Modelo()

    modelo.X_train = X
    modelo.y_train = y

    trained_model = modelo.apply_model()

    assert trained_model is not None
    assert hasattr(trained_model, "predict")
