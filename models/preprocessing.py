"""Módulo de pré-processamento de dados de vinhos."""

import pandas as pd
from sklearn.model_selection import train_test_split


class Preprocessing:
    """
    Classe para pré-processamento de dados de vinhos.

    Realiza leitura, concatenação, categorização de qualidade,
    seleção de features e divisão dos dados em treino e teste.
    """

    def __init__(self) -> None:
        """Inicializa a classe Preprocessing."""
        pass

    def leitura_dataset(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Lê os arquivos CSV de vinho tinto e branco.

        Returns:
            Tupla contendo (df_red, df_white), os DataFrames de
            vinho tinto e branco.

        Raises:
            FileNotFoundError: Se os arquivos CSV não forem encontrados
                nos caminhos especificados.
            pd.errors.ParserError: Se houver erro ao parsear os
                arquivos CSV.
        """
        self.df_red = pd.read_csv("src/winequality-red.csv", sep=";")
        self.df_white = pd.read_csv("src/winequality-white.csv", sep=";")
        return self.df_red, self.df_white

    def join_datasets(self) -> pd.DataFrame:
        """
        Concatena os datasets de vinho tinto e branco.

        Se os DataFrames ainda não foram carregados, chama
        automaticamente o método leitura_dataset().

        Returns:
            DataFrame único contendo todos os dados de vinhos tinto
            e branco concatenados.

        Raises:
            ValueError: Se houver inconsistência nas colunas dos
                DataFrames ao concatenar.
        """
        if self.df_red is None or self.df_white is None:
            self.leitura_dataset()
        self.data = pd.concat([self.df_red, self.df_white], ignore_index=True)
        return self.data

    def apply_categoria(self) -> pd.Series:
        """
        Converte a variável 'quality' em categorias numéricas discretas.

        Categorização:
        - 0 (Ruim): quality <= 5
        - 1 (Média): 5 < quality < 7
        - 2 (Boa): quality >= 7

        Returns:
            Série contendo as categorias de qualidade (0, 1 ou 2).

        Raises:
            KeyError: Se a coluna 'quality' não existir no DataFrame.
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
        Seleciona as features e a variável alvo para o modelo.

        Features selecionadas:
        - volatile acidity
        - density
        - alcohol
        - total sulfur dioxide
        - chlorides
        - sulphates

        Returns:
            Tupla contendo (X, y), onde X é o DataFrame de features
            e y é a Series da variável alvo.

        Raises:
            KeyError: Se alguma das colunas especificadas não existir
                no DataFrame.
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
        Divide os dados em conjuntos de treino e teste.

        Args:
            test_size: Proporção dos dados destinados ao conjunto de
                teste. Padrão é 0.2 (20% para teste, 80% para treino).
            random_state: Seed para reprodutibilidade da divisão
                aleatória. Padrão é 42.

        Returns:
            Tupla contendo (X_train, X_test, y_train, y_test),
            os conjuntos de treino e teste.

        Raises:
            ValueError: Se test_size não estiver entre 0 e 1, ou se
                houver problemas com a estratificação.
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
        Executa o pipeline completo de pré-processamento de dados.

        O pipeline inclui:
        1. Leitura dos datasets de vinho tinto e branco
        2. Concatenação dos datasets
        3. Aplicação de categorização na variável qualidade
        4. Seleção de features
        5. Divisão de dados em treino e teste

        Args:
            test_size: Proporção dos dados para teste. Padrão é 0.2.
            random_state: Seed para reprodutibilidade. Padrão é 42.

        Returns:
            Tupla contendo (X_train, X_test, y_train, y_test).
        """
        self.leitura_dataset()
        self.join_datasets()
        self.apply_categoria()
        self.feature_selection()
        self.split_dados(test_size=test_size, random_state=random_state)
        return self.X_train, self.X_test, self.y_train, self.y_test
