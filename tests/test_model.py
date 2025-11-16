"""Testes unitários para o módulo de treinamento de modelos."""

import json
from pathlib import Path

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


def test_evaluate_model_sem_dados() -> None:
    """
    Testa o comportamento ao tentar avaliar modelo sem dados de teste.

    Verifica se ValueError é lançado quando tentamos avaliar um modelo
    sem ter preparado os dados de teste (X_test e y_test) previamente.

    Raises:
        ValueError: Quando os dados de teste não estão disponíveis.

    Asserts:
        - A mensagem de erro contém "não disponíveis"
    """
    modelo = Modelo()

    with pytest.raises(ValueError) as exc_info:
        modelo.evaluate_model()

    assert "não disponíveis" in str(exc_info.value)


def test_evaluate_model_retorna_metricas(
    prepared_train_data: tuple[pd.DataFrame, pd.Series],
) -> None:
    """
    Testa se evaluate_model retorna métricas de avaliação corretas.

    Verifica se o método evaluate_model retorna um dicionário contendo
    todas as métricas esperadas (accuracy, f1_score, classification_report)
    após o modelo ser treinado com dados válidos.

    Args:
        prepared_train_data: Tupla com (X, y) preparados (fixture).

    Asserts:
        - O retorno é um dicionário
        - Contém chave "accuracy"
        - Contém chave "f1_score_weighted"
        - Contém chave "classification_report"
        - accuracy é um float entre 0 e 1
        - f1_score_weighted é um float entre 0 e 1
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
    Testa se save_model cria arquivo no caminho especificado.

    Verifica se o método save_model cria corretamente um arquivo .joblib
    no caminho fornecido e se esse arquivo existe após o salvamento.

    Args:
        temp_model_path: Caminho temporário para salvar o modelo (fixture).

    Asserts:
        - O arquivo é criado
        - O arquivo existe no caminho especificado
    """
    modelo = Modelo()

    modelo.save_model(str(temp_model_path))

    assert temp_model_path.exists()


def test_save_model_caminho_padrao() -> None:
    """
    Testa se save_model usa caminho padrão quando filepath é None.

    Verifica se o método save_model cria um arquivo com o nome padrão
    'random_forest_model.joblib' na pasta 'models/' quando nenhum
    caminho é fornecido.

    Asserts:
        - O método executa sem erros
        - Não lança exceção
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
    Testa se save_metadata cria arquivo JSON com metadados corretos.

    Verifica se o método save_metadata cria um arquivo JSON válido
    contendo todas as informações esperadas sobre o modelo, treinamento
    e performance.

    Args:
        tmp_path: Diretório temporário fornecido pelo pytest.
        prepared_train_data: Tupla com (X, y) preparados (fixture).

    Asserts:
        - O arquivo JSON é criado
        - O arquivo existe no caminho especificado
        - O JSON contém chave "model"
        - O JSON contém chave "training"
        - O JSON contém chave "performance"
        - Os metadados de performance estão corretos
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
