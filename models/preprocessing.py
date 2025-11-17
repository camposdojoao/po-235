"""Wine data preprocessing module."""

import pandas as pd
from sklearn.model_selection import train_test_split


class Preprocessing:
    """
    Class for wine data preprocessing.

    Performs reading, concatenation, quality categorization,
    feature selection, and train-test data splitting.
    """

    def __init__(self) -> None:
        """Initialize the Preprocessing class."""
        pass

    def leitura_dataset(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Read the red and white wine CSV files.

        Returns:
            Tuple containing (df_red, df_white), the DataFrames of
            red and white wines.

        Raises:
            FileNotFoundError: If the CSV files are not found
                in the specified paths.
            pd.errors.ParserError: If there is an error parsing the
                CSV files.
        """
        self.df_red = pd.read_csv("src/winequality-red.csv", sep=";")
        self.df_white = pd.read_csv("src/winequality-white.csv", sep=";")
        return self.df_red, self.df_white

    def join_datasets(self) -> pd.DataFrame:
        """
        Concatenate the red and white wine datasets.

        If the DataFrames have not been loaded yet, automatically
        calls the leitura_dataset() method.

        Returns:
            Single DataFrame containing all concatenated red and
            white wine data.

        Raises:
            ValueError: If there is inconsistency in DataFrame
                columns when concatenating.
        """
        if self.df_red is None or self.df_white is None:
            self.leitura_dataset()
        self.data = pd.concat([self.df_red, self.df_white], ignore_index=True)
        return self.data

    def apply_categoria(self) -> pd.Series:
        """
        Convert the 'quality' variable into discrete numeric categories.

        Categorization:
        - 0 (Poor): quality <= 5
        - 1 (Average): 5 < quality < 7
        - 2 (Good): quality >= 7

        Returns:
            Series containing quality categories (0, 1, or 2).

        Raises:
            KeyError: If the 'quality' column does not exist in the DataFrame.
        """
        if self.data is None:
            self.join_datasets()
        self.data["quality"] = self.data["quality"].apply(
            lambda q: 2 if q >= 7 else (1 if q > 5 else 0)
        )
        self.y = self.data["quality"]
        return self.y

    def feature_selection(self) -> tuple[pd.DataFrame, pd.Series]:
        """
        Select the features and target variable for the model.

        Selected features:
        - volatile acidity
        - density
        - alcohol
        - total sulfur dioxide
        - chlorides
        - sulphates

        Returns:
            Tuple containing (X, y), where X is the features DataFrame
            and y is the target variable Series.

        Raises:
            KeyError: If any of the specified columns does not exist
                in the DataFrame.
        """
        if self.data is None:
            self.join_datasets()
        if self.y is None:
            self.apply_categoria()
        self.X = self.data[
            [
                "volatile acidity",
                "density",
                "alcohol",
                "total sulfur dioxide",
                "chlorides",
                "sulphates",
            ]
        ]
        self.y = self.data["quality"]
        return self.X, self.y

    def split_dados(
        self, test_size: float = 0.2, random_state: int = 42
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
        Split the data into training and test sets.

        Args:
            test_size: Proportion of data for the test set.
                Default is 0.2 (20% for test, 80% for training).
            random_state: Seed for reproducibility of the random split.
                Default is 42.

        Returns:
            Tuple containing (X_train, X_test, y_train, y_test),
            the training and test sets.

        Raises:
            ValueError: If test_size is not between 0 and 1, or if
                there are problems with stratification.
        """
        if self.X is None or self.y is None:
            self.feature_selection()
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X,
            self.y,
            test_size=test_size,
            random_state=random_state,
            stratify=self.y,
        )
        return self.X_train, self.X_test, self.y_train, self.y_test

    def preprocess(
        self, test_size: float = 0.2, random_state: int = 42
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
        Execute the complete data preprocessing pipeline.

        The pipeline includes:
        1. Reading the red and white wine datasets
        2. Concatenating the datasets
        3. Applying categorization to the quality variable
        4. Feature selection
        5. Splitting data into training and test sets

        Args:
            test_size: Proportion of data for testing. Default is 0.2.
            random_state: Seed for reproducibility. Default is 42.

        Returns:
            Tuple containing (X_train, X_test, y_train, y_test).
        """
        self.leitura_dataset()
        self.join_datasets()
        self.apply_categoria()
        self.feature_selection()
        self.split_dados(test_size=test_size, random_state=random_state)
        return self.X_train, self.X_test, self.y_train, self.y_test
