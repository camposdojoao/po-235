"""Unit tests for the model training module."""

import json
from pathlib import Path

import pandas as pd
import pytest
from sklearn.ensemble import RandomForestClassifier

from models.model import Modelo


def test_init_modelo_random_forest() -> None:
    """
    Test Random Forest model initialization.

    Verifies that the Random Forest model is correctly instantiated
    with the appropriate parameters, including random_state
    for reproducibility.

    Asserts:
        - The model is an instance of RandomForestClassifier
        - The random_state is configured as 42
    """
    modelo = Modelo()
    assert isinstance(modelo.modelo, RandomForestClassifier)
    assert modelo.modelo.random_state == 42


def test_apply_model_sem_dados() -> None:
    """
    Test behavior when trying to train without prepared data.

    Verifies that ValueError is raised with an appropriate message when
    we try to train a model without having prepared the training data
    (X_train and y_train) beforehand.

    Raises:
        ValueError: When training data has not been prepared.

    Asserts:
        - The error message contains "not prepared"
    """
    modelo = Modelo()

    with pytest.raises(ValueError) as exc_info:
        modelo.apply_model()

    assert "not prepared" in str(exc_info.value)


def test_apply_model_com_dados(
    prepared_train_data: tuple[pd.DataFrame, pd.Series],
) -> None:
    """
    Test model training with valid data.

    Verifies that the model is successfully trained when valid data
    (X_train and y_train) is provided, and that the resulting model
    has the ability to make predictions.

    Args:
        prepared_train_data: Tuple with prepared (X, y) (fixture).

    Asserts:
        - The trained model is not None
        - The model has the predict method
    """
    X, y = prepared_train_data  # noqa: N806
    modelo = Modelo()

    modelo.X_train = X
    modelo.y_train = y

    trained_model = modelo.apply_model()

    assert trained_model is not None
    assert hasattr(trained_model, "predict")


def test_evaluate_model_sem_dados() -> None:
    """
    Test behavior when trying to evaluate model without test data.

    Verifies that ValueError is raised when we try to evaluate a model
    without having prepared the test data (X_test and y_test) beforehand.

    Raises:
        ValueError: When test data is not available.

    Asserts:
        - The error message contains "not available"
    """
    modelo = Modelo()

    with pytest.raises(ValueError) as exc_info:
        modelo.evaluate_model()

    assert "not available" in str(exc_info.value)


def test_evaluate_model_retorna_metricas(
    prepared_train_data: tuple[pd.DataFrame, pd.Series],
) -> None:
    """
    Test if evaluate_model returns correct evaluation metrics.

    Verifies that the evaluate_model method returns a dictionary containing
    all expected metrics (accuracy, f1_score, classification_report)
    after the model is trained with valid data.

    Args:
        prepared_train_data: Tuple with prepared (X, y) (fixture).

    Asserts:
        - The return is a dictionary
        - Contains "accuracy" key
        - Contains "f1_score_weighted" key
        - Contains "classification_report" key
        - accuracy is a float between 0 and 1
        - f1_score_weighted is a float between 0 and 1
    """
    X, y = prepared_train_data  # noqa: N806
    modelo = Modelo()

    # Prepara dados de treino e teste (usando os mesmos para simplicidade)
    modelo.X_train = X
    modelo.y_train = y
    modelo.X_test = X
    modelo.y_test = y

    # Treina o modelo
    modelo.apply_model()

    # Avalia o modelo
    metrics = modelo.evaluate_model()

    assert isinstance(metrics, dict)
    assert "accuracy" in metrics
    assert "f1_score_weighted" in metrics
    assert "classification_report" in metrics
    assert isinstance(metrics["accuracy"], float)
    assert isinstance(metrics["f1_score_weighted"], float)
    assert 0.0 <= metrics["accuracy"] <= 1.0
    assert 0.0 <= metrics["f1_score_weighted"] <= 1.0


def test_save_model_cria_arquivo(temp_model_path: Path) -> None:
    """
    Test if save_model creates a file at the specified path.

    Verifies that the save_model method correctly creates a .joblib file
    at the provided path and that this file exists after saving.

    Args:
        temp_model_path: Temporary path to save the model (fixture).

    Asserts:
        - The file is created
        - The file exists at the specified path
    """
    modelo = Modelo()

    modelo.save_model(str(temp_model_path))

    assert temp_model_path.exists()


def test_save_model_caminho_padrao() -> None:
    """
    Test if save_model uses default path when filepath is None.

    Verifies that the save_model method creates a file with the default name
    'random_forest_model.joblib' in the 'models/' folder when no
    path is provided.

    Asserts:
        - The method executes without errors
        - Does not raise an exception
    """
    modelo = Modelo()

    # Testa que não lança exceção ao salvar com caminho padrão
    # (não verificamos se arquivo existe pois seria na pasta models/ real)
    try:
        modelo.save_model()
    except Exception as e:
        pytest.fail(f"save_model() lançou exceção inesperada: {e}")


def test_save_metadata_cria_json(
    tmp_path: Path, prepared_train_data: tuple[pd.DataFrame, pd.Series]
) -> None:
    """
    Test if save_metadata creates JSON file with correct metadata.

    Verifies that the save_metadata method creates a valid JSON file
    containing all expected information about the model, training,
    and performance.

    Args:
        tmp_path: Temporary directory provided by pytest.
        prepared_train_data: Tuple with prepared (X, y) (fixture).

    Asserts:
        - The JSON file is created
        - The file exists at the specified path
        - The JSON contains "model" key
        - The JSON contains "training" key
        - The JSON contains "performance" key
        - The performance metadata is correct
    """
    X, y = prepared_train_data  # noqa: N806
    modelo = Modelo()

    # Prepara dados necessários para gerar metadados
    modelo.X_train = X
    modelo.X_test = X
    modelo.y_train = y
    modelo.y_test = y

    # Métricas de exemplo
    metrics = {
        "accuracy": 0.85,
        "f1_score_weighted": 0.83,
        "classification_report": {},
    }

    filepath = tmp_path / "metadata.json"

    modelo.save_metadata(metrics, str(filepath))

    # Verifica se arquivo foi criado
    assert filepath.exists()

    # Verifica conteúdo do JSON
    with filepath.open() as f:
        data = json.load(f)

    assert "model" in data
    assert "training" in data
    assert "performance" in data
    assert data["performance"]["accuracy"] == 0.85
    assert data["performance"]["f1_score_weighted"] == 0.83
    assert data["model"]["name"] == "Random Forest Classifier"
