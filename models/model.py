"""Módulo de treinamento de modelo Random Forest para classificação de vinhos."""

import joblib
from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestClassifier

from models.preprocessing import Preprocessing


class Modelo:
    """
    Classe para treinamento e gerenciamento do modelo Random Forest.

    Utiliza a classe Preprocessing para preparar os dados e realiza o
    treinamento e salvamento do modelo Random Forest.
    """

    def __init__(self) -> None:
        """
        Inicializa a classe Modelo com Random Forest.

        Configura o preprocessamento e inicializa o modelo Random Forest
        com random_state=42 para reprodutibilidade.
        """
        self.preprocessing = Preprocessing()
        self.modelo = RandomForestClassifier(random_state=42)
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def apply_model(self) -> BaseEstimator:
        """
        Treina o modelo de machine learning com os dados de treino.

        Returns:
            Modelo treinado.

        Raises:
            ValueError: Se houver problemas com os dados de treino
                (ex: valores faltantes, tipos incompatíveis).
        """
        if self.X_train is None or self.y_train is None:
            raise ValueError(
                "Dados de treino não foram preparados. "
                "Execute o pré-processamento primeiro."
            )
        self.modelo.fit(self.X_train, self.y_train)
        return self.modelo

    def save_model(self, filepath: str | None = None) -> None:
        """
        Salva o modelo treinado em arquivo .joblib.

        Se filepath não for fornecido, salva como 'models/random_forest_model.joblib'.

        Args:
            filepath: Caminho do arquivo onde o modelo será salvo.
                Se None, usa o caminho padrão.

        Raises:
            IOError: Se houver problemas ao escrever o arquivo no disco.
            PermissionError: Se não houver permissão de escrita no
                diretório especificado.
        """
        if filepath is None:
            filepath = "models/random_forest_model.joblib"

        joblib.dump(self.modelo, filepath)
        print(f"Modelo salvo em: {filepath}")

    def train(self, test_size: float = 0.2, random_state: int = 42) -> None:
        """
        Executa o pipeline completo de treinamento do modelo.

        O pipeline inclui:
        1. Pré-processamento completo dos dados (leitura, concatenação,
           categorização, feature selection e split)
        2. Treinamento do modelo
        3. Salvamento do modelo treinado

        Args:
            test_size: Proporção dos dados para teste. Padrão é 0.2.
            random_state: Seed para reprodutibilidade. Padrão é 42.

        Raises:
            Exception: Qualquer exceção que possa ocorrer durante as
                etapas do pipeline.
        """
        # Executa o pré-processamento completo
        self.X_train, self.X_test, self.y_train, self.y_test = (
            self.preprocessing.preprocess(
                test_size=test_size, random_state=random_state
            )
        )

        # Treina o modelo
        self.apply_model()

        # Salva o modelo
        self.save_model()
