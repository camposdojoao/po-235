"""Módulo de treinamento de modelos de classificação de vinhos."""

from datetime import datetime

import joblib
from sklearn.base import BaseEstimator
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from xgboost import XGBClassifier

from models.preprocessing import Preprocessing


class Modelo:
    """
    Classe para treinamento e gerenciamento de modelo de classificação.

    Utiliza a classe Preprocessing para preparar os dados e realiza o
    treinamento e salvamento do modelo de machine learning.
    """

    # Lista de modelos disponíveis
    modelos = ["random_forest", "xgboost", "gradient_boosting"]

    def __init__(self, variavel: str) -> None:
        """
        Inicializa a classe Modelo com o tipo de modelo desejado.

        Args:
            variavel: Nome do modelo a ser utilizado.
                Opções: 'random_forest', 'xgboost', 'gradient_boosting'.

        Raises:
            ValueError: Se o modelo especificado não estiver disponível.
        """
        if variavel not in self.modelos:
            raise ValueError(
                f"Modelo '{variavel}' não encontrado. "
                f"Modelos disponíveis: {self.modelos}"
            )

        self.preprocessing = Preprocessing()
        self.modelo = self._selecionar_modelo(variavel)
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def _selecionar_modelo(self, variavel: str) -> BaseEstimator:
        """
        Seleciona e retorna a instância do modelo baseado no nome fornecido.

        Args:
            variavel: Nome do modelo a ser selecionado.

        Returns:
            Instância do modelo de machine learning.
        """
        if variavel == "random_forest":
            return RandomForestClassifier(random_state=42)
        elif variavel == "xgboost":
            return XGBClassifier(random_state=42)
        elif variavel == "gradient_boosting":
            return GradientBoostingClassifier(random_state=42)
        return RandomForestClassifier(random_state=42)

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

        Se filepath não for fornecido, gera automaticamente o nome do
        arquivo baseado no tipo do modelo e timestamp.

        Args:
            filepath: Caminho do arquivo onde o modelo será salvo.
                Se None, gera automaticamente baseado no tipo do modelo.

        Raises:
            IOError: Se houver problemas ao escrever o arquivo no disco.
            PermissionError: Se não houver permissão de escrita no
                diretório especificado.
        """
        if filepath is None:
            model_name = type(self.modelo).__name__
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"models/{model_name}_{timestamp}.joblib"

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
