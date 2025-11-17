"""Unit tests for the preprocessing module."""

import pandas as pd

from models.preprocessing import Preprocessing


def test_leitura_dataset() -> None:
    """
    Test reading of wine CSV files.

    Verifies that the red and white wine datasets are correctly read
    from CSV files, are valid DataFrames with data, and contain
    the 'quality' column necessary for training.

    Asserts:
        - Both returns are pandas DataFrames
        - Both DataFrames contain data (are not empty)
        - Both have the 'quality' column
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
    Test concatenation of red and white wine datasets.

    Verifies that the two datasets are correctly concatenated into a
    single DataFrame, maintaining all original rows and columns.

    Asserts:
        - The result is a pandas DataFrame
        - The total size is the sum of the individual dataset sizes
        - The 'quality' column is maintained after concatenation
    """
    preprocessing = Preprocessing()
    preprocessing.leitura_dataset()
    data = preprocessing.join_datasets()

    assert isinstance(data, pd.DataFrame)

    assert len(data) == len(preprocessing.df_red) + len(preprocessing.df_white)

    assert "quality" in data.columns


def test_apply_categoria() -> None:
    """
    Test application of categorization to the quality variable.

    Verifies that the continuous 'quality' variable is correctly converted
    into discrete categories:
    - 0 (Poor): quality <= 5
    - 1 (Average): 5 < quality < 7
    - 2 (Good): quality >= 7

    Asserts:
        - The result is a pandas Series
        - All values are in the set {0, 1, 2}
    """
    preprocessing = Preprocessing()
    preprocessing.leitura_dataset()
    preprocessing.join_datasets()
    y = preprocessing.apply_categoria()

    assert isinstance(y, pd.Series)

    assert set(y.unique()).issubset({0, 1, 2})


def test_feature_selection() -> None:
    """
    Test selection of relevant features for the model.

    Verifies that the 6 most important features are correctly selected
    from the complete dataset:
    - volatile acidity
    - density
    - alcohol
    - total sulfur dioxide
    - chlorides
    - sulphates

    Asserts:
        - X is a pandas DataFrame
        - y is a pandas Series
        - X contains exactly the 6 expected features in the correct order
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
    Test splitting of data into training and test sets.

    Verifies that the data is correctly split using stratification
    to maintain class proportions, and that the split follows the default
    80% training / 20% test ratio.

    Asserts:
        - All returns (X_train, X_test, y_train, y_test) have the correct type
        - The training proportion is between 75% and 85% (5% margin)
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
    Test the complete preprocessing pipeline.

    Verifies that the preprocess() method executes all preprocessing
    steps correctly in sequence:
    1. Reading datasets
    2. Concatenation
    3. Quality categorization
    4. Feature selection
    5. Train/test split

    Args:
        None - uses the actual wine datasets.

    Asserts:
        - All returns are of the correct type
        - X_train and X_test contain data
        - The correct features are present in X_train

    Note:
        This is an integration test that validates the complete pipeline.
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
