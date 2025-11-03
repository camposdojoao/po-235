"""Módulo de inferência de modelos de classificação de vinhos."""

import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator


class Inferences:
    """
    Classe para realizar inferências com modelos treinados.

    Gerencia o carregamento de modelos salvos e realiza predições.
    """

    def __init__(self) -> None:
        """Inicializa a classe Inferences."""
        self.modelo: BaseEstimator | None = None

    def load_model(self, filepath: str) -> BaseEstimator:
        """
        Carrega um modelo previamente treinado e salvo em arquivo .joblib.

        Args:
            filepath: Caminho do arquivo .joblib contendo o modelo treinado.

        Returns:
            Modelo carregado do arquivo.

        Raises:
            FileNotFoundError: Se o arquivo especificado não for encontrado.
            pickle.UnpicklingError: Se houver erro ao desserializar o
                arquivo .joblib.
        """
        self.modelo = joblib.load(filepath)
        print(f"Modelo carregado de: {filepath}")
        return self.modelo

    def model_predict(self, features: pd.DataFrame | np.ndarray) -> np.ndarray:
        """
        Realiza previsões usando o modelo treinado.

        Args:
            features: Features para realizar previsões.

        Returns:
            Array com as previsões do modelo.

        Raises:
            ValueError: Se o modelo ainda não foi treinado.
        """
        if self.modelo is None:
            raise ValueError("Modelo não foi carregado ainda.")
        return self.modelo.predict(features)
