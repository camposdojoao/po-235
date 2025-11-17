"""Inference module for wine classification models."""

import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator


class Inferences:
    """
    Class for performing inferences with trained models.

    Manages loading of saved models and performs predictions.
    """

    def __init__(self) -> None:
        """Initialize the Inferences class."""
        self.modelo: BaseEstimator | None = None

    def load_model(self, filepath: str) -> BaseEstimator:
        """
        Load a previously trained model saved in a .joblib file.

        Args:
            filepath: Path to the .joblib file containing the trained model.

        Returns:
            Model loaded from the file.

        Raises:
            FileNotFoundError: If the specified file is not found.
            pickle.UnpicklingError: If there is an error deserializing the
                .joblib file.
        """
        self.modelo = joblib.load(filepath)
        print(f"Modelo carregado de: {filepath}")
        return self.modelo

    def model_predict(self, features: pd.DataFrame | np.ndarray) -> np.ndarray:
        """
        Perform predictions using the trained model.

        Args:
            features: Features for making predictions.

        Returns:
            Array with model predictions.

        Raises:
            ValueError: If the model has not been loaded yet.
        """
        if self.modelo is None:
            raise ValueError("Model not loaded yet.")
        return self.modelo.predict(features)
