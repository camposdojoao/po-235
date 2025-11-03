"""Fixtures compartilhadas para os testes."""

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
    Cria dados de vinho de exemplo para testes.

    Retorna um DataFrame contendo um pequeno conjunto de dados de vinhos
    com todas as features necessárias e valores de qualidade variados
    para testar a categorização.

    Returns:
        DataFrame com 5 amostras de vinhos com todas as features e qualidades
        variadas (5, 5, 5, 6, 8) para testar diferentes categorias.

    Note:
        Os valores de qualidade são escolhidos para cobrir todas as categorias:
        - quality <= 5: categoria 0 (Ruim)
        - 5 < quality < 7: categoria 1 (Média)
        - quality >= 7: categoria 2 (Boa)
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
    Cria features de exemplo para testes de predição.

    Retorna um DataFrame contendo apenas as 6 features selecionadas
    para o modelo, com 3 amostras variadas para testar predições.

    Returns:
        DataFrame com 3 amostras contendo as 6 features selecionadas:
        volatile acidity, density, alcohol, total sulfur dioxide,
        chlorides e sulphates.

    Note:
        Este DataFrame contém apenas as features necessárias para
        fazer predições, sem incluir a coluna quality.
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
    Retorna um caminho temporário para salvar modelos de teste.

    Args:
        tmp_path: Diretório temporário fornecido pelo pytest.

    Returns:
        Path para um arquivo .joblib no diretório temporário.

    Note:
        O arquivo é automaticamente removido após o teste pelo pytest.
    """
    return tmp_path / "test_model.joblib"


@pytest.fixture
def prepared_train_data(
    sample_wine_data: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Prepara dados de treino (X, y) prontos para uso.

    Processa o DataFrame de vinhos para extrair as features selecionadas
    e a variável alvo categorizada, pronta para treinar modelos.

    Args:
        sample_wine_data: DataFrame com dados de vinhos de exemplo (fixture).

    Returns:
        Tupla contendo:
        - X (DataFrame): Features selecionadas para o modelo
        - y (Series): Variável alvo categorizada (0, 1 ou 2)

    Note:
        As categorias de qualidade seguem a regra:
        - 0 (Ruim): quality <= 5
        - 1 (Média): 5 < quality < 7
        - 2 (Boa): quality >= 7
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
    Cria, treina e salva um modelo RandomForest para testes.

    Treina um modelo RandomForestClassifier com os dados de exemplo
    e salva o modelo treinado em um arquivo temporário.

    Args:
        prepared_train_data: Tupla com (X, y) preparados (fixture).
        temp_model_path: Caminho temporário para salvar o modelo (fixture).

    Returns:
        Path para o arquivo .joblib contendo o modelo treinado.

    Note:
        O modelo é treinado com random_state=42 para reprodutibilidade.
        O arquivo é automaticamente removido após o teste pelo pytest.
    """
    X, y = prepared_train_data  # noqa: N806

    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)

    joblib.dump(model, str(temp_model_path))

    return temp_model_path


@pytest.fixture
def streamlit_mocks() -> Generator[dict[str, object]]:
    """
    Configura mocks para Streamlit e seus componentes.

    Cria mocks para os componentes principais do Streamlit (session_state,
    Models e Sidebar) permitindo testar o entrypoint sem inicializar
    o servidor Streamlit real.

    Yields:
        Dicionário contendo os mocks configurados:
        - session_state: Mock do estado da sessão Streamlit
        - MockModels: Mock da classe Models
        - MockSidebar: Mock da classe Sidebar
        - sidebar_instance: Instância mockada do Sidebar
        - models_instance: Instância mockada do Models

    Note:
        O mock de session_state é configurado com view="models" por padrão.
        Todos os mocks são automaticamente limpos após o teste.
    """
    mock_session_state = {"view": "models"}

    with patch("streamlit.session_state", mock_session_state):
        with patch("streamlit_app.models.Models") as mock_models:  # noqa: N806
            with patch("streamlit_app.sidebar.Sidebar") as mock_sidebar:  # noqa: N806
                mock_sidebar_instance = MagicMock()
                mock_sidebar.return_value = mock_sidebar_instance

                mock_models_instance = MagicMock()
                mock_models.return_value = mock_models_instance

                yield {
                    "session_state": mock_session_state,
                    "MockModels": mock_models,
                    "MockSidebar": mock_sidebar,
                    "sidebar_instance": mock_sidebar_instance,
                    "models_instance": mock_models_instance,
                }


@pytest.fixture
def train_mocks() -> Generator[dict[str, object]]:
    """
    Configura mocks para o entrypoint de treinamento.

    Cria mocks para a classe Modelo permitindo testar o entrypoint
    de treinamento sem executar o treinamento real do modelo, que
    seria demorado e desnecessário para testes unitários.

    Yields:
        Dicionário contendo os mocks configurados:
        - MockModelo: Mock da classe Modelo
        - modelo_instance: Instância mockada do Modelo

    Note:
        A instância mockada possui o método train() configurado,
        permitindo verificar se foi chamado corretamente.
        Todos os mocks são automaticamente limpos após o teste.
    """
    with patch("entrypoints.train.Modelo") as mock_modelo:  # noqa: N806
        mock_instance = MagicMock()
        mock_modelo.return_value = mock_instance

        yield {
            "MockModelo": mock_modelo,
            "modelo_instance": mock_instance,
        }
