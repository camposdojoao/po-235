"""Random Forest model training module for wine classification."""

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
    Class for training and managing the Random Forest model.

    Uses the Preprocessing class to prepare data and performs
    training and saving of the Random Forest model.
    """

    def __init__(self) -> None:
        """
        Initialize the Modelo class with Random Forest.

        Configures preprocessing and initializes the Random Forest model
        with random_state=42 for reproducibility.
        """
        self.preprocessing = Preprocessing()
        self.modelo = RandomForestClassifier(random_state=42)
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def apply_model(self) -> BaseEstimator:
        """
        Train the machine learning model with the training data.

        Returns:
            Trained model.

        Raises:
            ValueError: If there are problems with the training data
                (e.g., missing values, incompatible types).
        """
        if self.X_train is None or self.y_train is None:
            raise ValueError("Training data not prepared. Execute preprocessing first.")
        self.modelo.fit(self.X_train, self.y_train)
        return self.modelo

    def evaluate_model(self) -> dict:
        """
        Evaluate the trained model using the test set.

        Calculates performance metrics including accuracy, f1-score,
        and detailed classification report.

        Returns:
            Dictionary containing evaluation metrics.

        Raises:
            ValueError: If the model was not trained or test data
                is not available.
        """
        if self.X_test is None or self.y_test is None:
            raise ValueError("Test data not available. Execute preprocessing first.")

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
        Save the trained model to a .joblib file.

        If filepath is not provided, saves as 'models/random_forest_model.joblib'.

        Args:
            filepath: Path to the file where the model will be saved.
                If None, uses the default path.

        Raises:
            IOError: If there are problems writing the file to disk.
            PermissionError: If there is no write permission in the
                specified directory.
        """
        if filepath is None:
            filepath = "models/random_forest_model.joblib"

        joblib.dump(self.modelo, filepath)
        print(f"Modelo salvo em: {filepath}")

    def save_metadata(
        self, metrics: dict, filepath: str = "models/model_metadata.json"
    ) -> None:
        """
        Save model metadata to a JSON file.

        Args:
            metrics: Dictionary containing model evaluation metrics.
            filepath: Path where the JSON file will be saved.

        Raises:
            IOError: If there are problems writing the file to disk.
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

        with Path(filepath).open("w") as f:
            json.dump(metadata, f, indent=2)

        print(f"Metadados salvos em: {filepath}")

    def train(self, test_size: float = 0.2, random_state: int = 42) -> None:
        """
        Execute the complete model training pipeline.

        The pipeline includes:
        1. Complete data preprocessing (reading, concatenation,
           categorization, feature selection, and split)
        2. Model training
        3. Model evaluation
        4. Saving model and metadata

        Args:
            test_size: Proportion of data for testing. Default is 0.2.
            random_state: Seed for reproducibility. Default is 42.

        Raises:
            Exception: Any exception that may occur during the
                pipeline steps.
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
        print(
            f"✓ Dados preparados: {len(self.X_train)} treino, {len(self.X_test)} teste"
        )

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
