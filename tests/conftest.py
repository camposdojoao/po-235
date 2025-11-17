"""Shared fixtures for tests."""

import sys
from collections.abc import Generator
from pathlib import Path
from unittest.mock import MagicMock, patch

import joblib
import pandas as pd
import pytest
from sklearn.ensemble import RandomForestClassifier

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


@pytest.fixture
def sample_wine_data() -> pd.DataFrame:
    """
    Create sample wine data for testing.

    Returns a DataFrame containing a small wine dataset
    with all necessary features and varied quality values
    to test categorization.

    Returns:
        DataFrame with 5 wine samples with all features and varied
        qualities (5, 5, 5, 6, 8) to test different categories.

    Note:
        Quality values are chosen to cover all categories:
        - quality <= 5: category 0 (Poor)
        - 5 < quality < 7: category 1 (Average)
        - quality >= 7: category 2 (Good)
    """
    data = {
        "fixed acidity": [7.4, 7.8, 7.8, 11.2, 7.4],
        "volatile acidity": [0.7, 0.88, 0.76, 0.28, 0.7],
        "citric acid": [0.0, 0.0, 0.04, 0.56, 0.0],
        "residual sugar": [1.9, 2.6, 2.3, 1.9, 1.9],
        "chlorides": [0.076, 0.098, 0.092, 0.075, 0.076],
        "free sulfur dioxide": [11.0, 25.0, 15.0, 17.0, 11.0],
        "total sulfur dioxide": [34.0, 67.0, 54.0, 60.0, 34.0],
        "density": [0.9978, 0.9968, 0.997, 0.998, 0.9978],
        "pH": [3.51, 3.2, 3.26, 3.16, 3.51],
        "sulphates": [0.56, 0.68, 0.65, 0.58, 0.56],
        "alcohol": [9.4, 9.8, 9.8, 9.8, 9.4],
        "quality": [5, 5, 5, 6, 8],
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_features() -> pd.DataFrame:
    """
    Create sample features for prediction tests.

    Returns a DataFrame containing only the 6 selected features
    for the model, with 3 varied samples to test predictions.

    Returns:
        DataFrame with 3 samples containing the 6 selected features:
        volatile acidity, density, alcohol, total sulfur dioxide,
        chlorides, and sulphates.

    Note:
        This DataFrame contains only the features necessary for
        making predictions, without including the quality column.
    """
    data = {
        "volatile acidity": [0.7, 0.28, 0.5],
        "density": [0.998, 0.996, 0.997],
        "alcohol": [9.4, 11.2, 10.5],
        "total sulfur dioxide": [45.0, 60.0, 50.0],
        "chlorides": [0.076, 0.045, 0.060],
        "sulphates": [0.68, 0.58, 0.65],
    }
    return pd.DataFrame(data)


@pytest.fixture
def temp_model_path(tmp_path: Path) -> Path:
    """
    Return a temporary path for saving test models.

    Args:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        Path to a .joblib file in the temporary directory.

    Note:
        The file is automatically removed after the test by pytest.
    """
    return tmp_path / "test_model.joblib"


@pytest.fixture
def prepared_train_data(
    sample_wine_data: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Prepare training data (X, y) ready for use.

    Processes the wine DataFrame to extract selected features
    and the categorized target variable, ready for training models.

    Args:
        sample_wine_data: DataFrame with sample wine data (fixture).

    Returns:
        Tuple containing:
        - X (DataFrame): Selected features for the model
        - y (Series): Categorized target variable (0, 1, or 2)

    Note:
        Quality categories follow the rule:
        - 0 (Poor): quality <= 5
        - 1 (Average): 5 < quality < 7
        - 2 (Good): quality >= 7
    """
    X = sample_wine_data[  # noqa: N806
        [
            "volatile acidity",
            "density",
            "alcohol",
            "total sulfur dioxide",
            "chlorides",
            "sulphates",
        ]
    ]
    y = sample_wine_data["quality"].apply(
        lambda q: 2 if q >= 7 else (1 if q > 5 else 0)
    )

    return X, y


@pytest.fixture
def trained_model_path(
    prepared_train_data: tuple[pd.DataFrame, pd.Series], temp_model_path: Path
) -> Path:
    """
    Create, train, and save a RandomForest model for testing.

    Trains a RandomForestClassifier model with the sample data
    and saves the trained model to a temporary file.

    Args:
        prepared_train_data: Tuple with prepared (X, y) (fixture).
        temp_model_path: Temporary path to save the model (fixture).

    Returns:
        Path to the .joblib file containing the trained model.

    Note:
        The model is trained with random_state=42 for reproducibility.
        The file is automatically removed after the test by pytest.
    """
    X, y = prepared_train_data  # noqa: N806

    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)

    joblib.dump(model, str(temp_model_path))

    return temp_model_path


@pytest.fixture
def streamlit_mocks() -> Generator[dict[str, object]]:
    """
    Configure mocks for Streamlit and its components.

    Creates mocks for the main Streamlit components (Models)
    allowing testing of the entrypoint without initializing the actual Streamlit server.

    Yields:
        Dictionary containing the configured mocks:
        - MockModels: Mock of the Models class
        - models_instance: Mocked instance of Models

    Note:
        All mocks are automatically cleaned up after the test.
    """
    with patch("streamlit_app.models.Models") as mock_models:  # noqa: N806
        mock_models_instance = MagicMock()
        mock_models.return_value = mock_models_instance

        yield {
            "MockModels": mock_models,
            "models_instance": mock_models_instance,
        }


@pytest.fixture
def train_mocks() -> Generator[dict[str, object]]:
    """
    Configure mocks for the training entrypoint.

    Creates mocks for the Modelo class allowing testing of the training
    entrypoint without executing actual model training, which
    would be time-consuming and unnecessary for unit tests.

    Yields:
        Dictionary containing the configured mocks:
        - MockModelo: Mock of the Modelo class
        - modelo_instance: Mocked instance of Modelo

    Note:
        The mocked instance has the train() method configured,
        allowing verification of correct calls.
        All mocks are automatically cleaned up after the test.
    """
    with patch("entrypoints.train.Modelo") as mock_modelo:  # noqa: N806
        mock_instance = MagicMock()
        mock_modelo.return_value = mock_instance

        yield {
            "MockModelo": mock_modelo,
            "modelo_instance": mock_instance,
        }
