"""Testes unitários para o módulo de pré-processamento."""

import pandas as pd

from models.preprocessing import Preprocessing


def test_leitura_dataset() -> None:
    """
    Testa a leitura dos arquivos CSV de vinhos.

    Verifica se os datasets de vinho tinto e branco são lidos corretamente
    dos arquivos CSV, se são DataFrames válidos com dados, e se contêm
    a coluna 'quality' necessária para o treinamento.

    Asserts:
        - Ambos os retornos são DataFrames pandas
        - Ambos os DataFrames contêm dados (não estão vazios)
        - Ambos possuem a coluna 'quality'
    """
    preprocessing = Preprocessing()
    df_red, df_white = preprocessing.leitura_dataset()

    assert isinstance(df_red, pd.DataFrame)
    assert isinstance(df_white, pd.DataFrame)

    assert len(df_red) > 0
    assert len(df_white) > 0

    assert "quality" in df_red.columns
    assert "quality" in df_white.columns


def test_join_datasets() -> None:
    """
    Testa a concatenação dos datasets de vinho tinto e branco.

    Verifica se os dois datasets são concatenados corretamente em um
    único DataFrame, mantendo todas as linhas e colunas originais.

    Asserts:
        - O resultado é um DataFrame pandas
        - O tamanho total é a soma dos tamanhos dos datasets individuais
        - A coluna 'quality' é mantida após a concatenação
    """
    preprocessing = Preprocessing()
    preprocessing.leitura_dataset()
    data = preprocessing.join_datasets()

    assert isinstance(data, pd.DataFrame)

    assert len(data) == len(preprocessing.df_red) + len(preprocessing.df_white)

    assert "quality" in data.columns


def test_apply_categoria() -> None:
    """
    Testa a aplicação de categorização na variável quality.

    Verifica se a variável contínua 'quality' é convertida corretamente
    em categorias discretas:
    - 0 (Ruim): quality <= 5
    - 1 (Média): 5 < quality < 7
    - 2 (Boa): quality >= 7

    Asserts:
        - O resultado é uma Series pandas
        - Todos os valores estão no conjunto {0, 1, 2}
    """
    preprocessing = Preprocessing()
    preprocessing.leitura_dataset()
    preprocessing.join_datasets()
    y = preprocessing.apply_categoria()

    assert isinstance(y, pd.Series)

    assert set(y.unique()).issubset({0, 1, 2})


def test_feature_selection() -> None:
    """
    Testa a seleção das features relevantes para o modelo.

    Verifica se as 6 features mais importantes são selecionadas
    corretamente do dataset completo:
    - volatile acidity
    - density
    - alcohol
    - total sulfur dioxide
    - chlorides
    - sulphates

    Asserts:
        - X é um DataFrame pandas
        - y é uma Series pandas
        - X contém exatamente as 6 features esperadas na ordem correta
    """
    preprocessing = Preprocessing()
    preprocessing.leitura_dataset()
    preprocessing.join_datasets()
    preprocessing.apply_categoria()

    X, y = preprocessing.feature_selection()  # noqa: N806

    assert isinstance(X, pd.DataFrame)
    assert isinstance(y, pd.Series)

    expected_features = [
        "volatile acidity",
        "density",
        "alcohol",
        "total sulfur dioxide",
        "chlorides",
        "sulphates",
    ]
    assert list(X.columns) == expected_features


def test_split_dados() -> None:
    """
    Testa a divisão dos dados em conjuntos de treino e teste.

    Verifica se os dados são divididos corretamente usando estratificação
    para manter a proporção das classes, e se a divisão segue a proporção
    padrão de 80% treino / 20% teste.

    Asserts:
        - Todos os retornos (X_train, X_test, y_train, y_test) têm o tipo correto
        - A proporção de treino está entre 75% e 85% (margem de 5%)
    """
    preprocessing = Preprocessing()
    preprocessing.leitura_dataset()
    preprocessing.join_datasets()
    preprocessing.apply_categoria()
    preprocessing.feature_selection()

    X_train, X_test, y_train, y_test = preprocessing.split_dados()  # noqa: N806

    assert isinstance(X_train, pd.DataFrame)
    assert isinstance(X_test, pd.DataFrame)
    assert isinstance(y_train, pd.Series)
    assert isinstance(y_test, pd.Series)

    total_size = len(X_train) + len(X_test)
    train_proportion = len(X_train) / total_size
    assert 0.75 < train_proportion < 0.85


def test_preprocess() -> None:
    """
    Testa o pipeline completo de pré-processamento.

    Verifica se o método preprocess() executa todas as etapas de
    pré-processamento corretamente em sequência:
    1. Leitura dos datasets
    2. Concatenação
    3. Categorização de qualidade
    4. Seleção de features
    5. Divisão em treino/teste

    Args:
        Nenhum - usa os datasets reais de vinhos.

    Asserts:
        - Todos os retornos são do tipo correto
        - X_train e X_test contêm dados
        - As features corretas estão presentes em X_train

    Note:
        Este é um teste de integração que valida o pipeline completo.
    """
    preprocessing = Preprocessing()
    X_train, X_test, y_train, y_test = preprocessing.preprocess()  # noqa: N806

    assert isinstance(X_train, pd.DataFrame)
    assert isinstance(X_test, pd.DataFrame)
    assert isinstance(y_train, pd.Series)
    assert isinstance(y_test, pd.Series)

    assert len(X_train) > 0
    assert len(X_test) > 0

    expected_features = [
        "volatile acidity",
        "density",
        "alcohol",
        "total sulfur dioxide",
        "chlorides",
        "sulphates",
    ]
    assert list(X_train.columns) == expected_features
