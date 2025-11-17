"""Unit tests for the inferences module."""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.ensemble import RandomForestClassifier

from models.inferences import Inferences


def test_load_model(trained_model_path: Path) -> None:
    """
    Test loading a trained model from a file.

    Verifies that the model is correctly loaded from the .joblib file
    and is properly assigned to the instance attribute.

    Args:
        trained_model_path: Path to the trained model file (fixture).

    Asserts:
        - The loaded model is not None
        - The instance's modelo attribute is not None
        - The loaded model is an instance of RandomForestClassifier
    """
    inference = Inferences()
    loaded_model = inference.load_model(str(trained_model_path))

    assert loaded_model is not None
    assert inference.modelo is not None
    assert isinstance(inference.modelo, RandomForestClassifier)


def test_load_model_arquivo_inexistente() -> None:
    """
    Test behavior when trying to load model from non-existent file.

    Verifies that FileNotFoundError is raised when we try to load
    a model from a path that does not exist.

    Raises:
        FileNotFoundError: When the specified file does not exist.
    """
    inference = Inferences()

    with pytest.raises(FileNotFoundError):
        inference.load_model("caminho/inexistente/modelo.joblib")


def test_model_predict(sample_features: pd.DataFrame, trained_model_path: Path) -> None:
    """
    Test making predictions with valid data.

    Verifies that the model can make predictions after being loaded
    and returns a numpy array with the correct size.

    Args:
        sample_features: DataFrame with sample features (fixture).
        trained_model_path: Path to the trained model file (fixture).

    Asserts:
        - The predictions are not None
        - The predictions are a numpy array
        - The number of predictions matches the number of input samples
    """
    inference = Inferences()
    inference.load_model(str(trained_model_path))
    predictions = inference.model_predict(sample_features)

    assert predictions is not None
    assert isinstance(predictions, np.ndarray)
    assert len(predictions) == len(sample_features)


def test_model_predict_sem_modelo() -> None:
    """
    Test behavior when trying to make prediction without loading model.

    Verifies that ValueError is raised with an appropriate message when
    we try to make predictions without having loaded a model beforehand.

    Raises:
        ValueError: When the model has not been loaded before prediction.

    Asserts:
        - The error message contains "not loaded"
    """
    inference = Inferences()

    with pytest.raises(ValueError) as exc_info:
        inference.model_predict(pd.DataFrame({"col1": [1, 2, 3]}))

    assert "not loaded" in str(exc_info.value)


def test_model_predict_valores_validos(
    sample_features: pd.DataFrame, trained_model_path: Path
) -> None:
    """
    Test if predictions return only valid classification values.

    Verifies that all model predictions are within the expected
    set of classes {0, 1, 2}, which represent wine quality
    categories (Poor, Average, Good).

    Args:
        sample_features: DataFrame with sample features (fixture).
        trained_model_path: Path to the trained model file (fixture).

    Asserts:
        - All predictions belong to the set {0, 1, 2}

    Raises:
        AssertionError: If there are predictions outside the valid set.
    """
    inference = Inferences()
    inference.load_model(str(trained_model_path))
    predictions = inference.model_predict(sample_features)

    unique_predictions = set(predictions)
    assert unique_predictions.issubset({0, 1, 2}), (
        f"Predictions must be 0, 1, or 2, but got: {unique_predictions}"
    )
