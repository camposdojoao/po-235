"""Módulo de treinamento de modelo Random Forest para classificação de vinhos."""

import json
from datetime import datetime
from pathlib import Path

import joblib
from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, f1_score

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

    def evaluate_model(self) -> dict:
        """
        Avalia o modelo treinado usando o conjunto de teste.

        Calcula métricas de performance incluindo accuracy, f1-score
        e classification report detalhado.

        Returns:
            Dicionário contendo as métricas de avaliação.

        Raises:
            ValueError: Se o modelo não foi treinado ou dados de teste
                não estão disponíveis.
        """
        if self.X_test is None or self.y_test is None:
            raise ValueError(
                "Dados de teste não disponíveis. "
                "Execute o pré-processamento primeiro."
            )

        # Fazer predições no conjunto de teste
        y_pred = self.modelo.predict(self.X_test)

        # Calcular métricas
        accuracy = accuracy_score(self.y_test, y_pred)
        f1 = f1_score(self.y_test, y_pred, average="weighted")

        # Gerar relatório de classificação
        report = classification_report(self.y_test, y_pred, output_dict=True)

        metrics = {
            "accuracy": float(accuracy),
            "f1_score_weighted": float(f1),
            "classification_report": report,
        }

        return metrics

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

    def save_metadata(
        self, metrics: dict, filepath: str = "models/model_metadata.json"
    ) -> None:
        """
        Salva metadados do modelo em arquivo JSON.

        Args:
            metrics: Dicionário contendo métricas de avaliação do modelo.
            filepath: Caminho onde o arquivo JSON será salvo.

        Raises:
            IOError: Se houver problemas ao escrever o arquivo no disco.
        """
        # Garantir que o diretório existe
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

        metadata = {
            "model": {
                "name": "Random Forest Classifier",
                "type": type(self.modelo).__name__,
                "sklearn_version": "1.7.2",
                "random_state": 42,
            },
            "training": {
                "timestamp": datetime.now().isoformat(),
                "dataset": {
                    "total_samples": len(self.X_train) + len(self.X_test),
                    "train_samples": len(self.X_train),
                    "test_samples": len(self.X_test),
                    "train_test_split": 0.2,
                },
                "features": list(self.X_train.columns),
            },
            "performance": metrics,
        }

        with open(filepath, "w") as f:
            json.dump(metadata, f, indent=2)

        print(f"Metadados salvos em: {filepath}")

    def train(self, test_size: float = 0.2, random_state: int = 42) -> None:
        """
        Executa o pipeline completo de treinamento do modelo.

        O pipeline inclui:
        1. Pré-processamento completo dos dados (leitura, concatenação,
           categorização, feature selection e split)
        2. Treinamento do modelo
        3. Avaliação do modelo
        4. Salvamento do modelo e metadados

        Args:
            test_size: Proporção dos dados para teste. Padrão é 0.2.
            random_state: Seed para reprodutibilidade. Padrão é 42.

        Raises:
            Exception: Qualquer exceção que possa ocorrer durante as
                etapas do pipeline.
        """
        print("=" * 60)
        print("Iniciando pipeline de treinamento")
        print("=" * 60)

        # Executa o pré-processamento completo
        print("\n[1/4] Executando pré-processamento dos dados...")
        self.X_train, self.X_test, self.y_train, self.y_test = (
            self.preprocessing.preprocess(
                test_size=test_size, random_state=random_state
            )
        )
        print(f"✓ Dados preparados: {len(self.X_train)} treino, {len(self.X_test)} teste")

        # Treina o modelo
        print("\n[2/4] Treinando modelo Random Forest...")
        self.apply_model()
        print("✓ Modelo treinado com sucesso")

        # Avalia o modelo
        print("\n[3/4] Avaliando modelo...")
        metrics = self.evaluate_model()
        print(f"✓ Acurácia: {metrics['accuracy']:.4f}")
        print(f"✓ F1-Score (weighted): {metrics['f1_score_weighted']:.4f}")

        # Salva o modelo e metadados
        print("\n[4/4] Salvando modelo e metadados...")
        self.save_model()
        self.save_metadata(metrics)

        print("\n" + "=" * 60)
        print("Pipeline de treinamento concluído!")
        print("=" * 60)
