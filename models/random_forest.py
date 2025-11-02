import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

class Modelo:
    """
    Classe para treinamento e gerenciamento de modelo de classificação de vinhos.
    
    Realiza o processamento completo desde a leitura dos datasets de vinho tinto e branco,
    categorização de qualidade, seleção de features, treinamento e salvamento do modelo.
    """
    
    def __init__(self, path_wine_red, path_wine_white, modelo):
        """
        Inicializa a classe Modelo com os caminhos dos datasets e o modelo a ser treinado.
        
        Args:
            path_wine_red (str): Caminho para o arquivo CSV do dataset de vinho tinto.
            path_wine_white (str): Caminho para o arquivo CSV do dataset de vinho branco.
            modelo (sklearn.base.BaseEstimator): Instância do modelo de machine learning a ser treinado.
        
        Returns:
            None
        """
        self.path_wine_red = path_wine_red
        self.path_wine_white = path_wine_white
        self.df_red = None
        self.df_white = None
        self.data = None
        self.X = None
        self.y = None
        self.modelo = modelo
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def leitura_dataset(self):
        """
        Lê os arquivos CSV de vinho tinto e branco e carrega em DataFrames.
        
        Args:
            None
        
        Returns:
            tuple: Tupla contendo (df_red, df_white), os DataFrames de vinho tinto e branco.
        
        Raises:
            FileNotFoundError: Se os arquivos CSV não forem encontrados nos caminhos especificados.
            pd.errors.ParserError: Se houver erro ao parsear os arquivos CSV.
        """
        self.df_red = pd.read_csv(self.path_wine_red, sep=';')
        self.df_white = pd.read_csv(self.path_wine_white, sep=';')
        return self.df_red, self.df_white

    def join_datasets(self):
        """
        Concatena os datasets de vinho tinto e branco em um único DataFrame.
        
        Se os DataFrames ainda não foram carregados, chama automaticamente o método leitura_dataset().
        
        Args:
            None
        
        Returns:
            pd.DataFrame: DataFrame único contendo todos os dados de vinhos tinto e branco concatenados.
        
        Raises:
            ValueError: Se houver inconsistência nas colunas dos DataFrames ao concatenar.
        """
        if self.df_red is None or self.df_white is None:
            self.leitura_dataset()
        self.data = pd.concat([self.df_red, self.df_white], ignore_index=True)
        return self.data

    def apply_categoria(self):
        """
        Converte a variável 'quality' em categorias numéricas discretas.
        
        Categorização:
        - 0 (Ruim): quality <= 5
        - 1 (Média): 5 < quality < 7
        - 2 (Boa): quality >= 7
        
        Args:
            None
        
        Returns:
            pd.Series: Série contendo as categorias de qualidade (0, 1 ou 2).
        
        Raises:
            KeyError: Se a coluna 'quality' não existir no DataFrame.
        """
        if self.data is None:
            self.join_datasets()
        self.data['quality'] = self.data['quality'].apply(
            lambda q: 2 if q >= 7 else (1 if q > 5 else 0)
        )
        self.y = self.data['quality']
        return self.y

    def feature_selection(self):
        """
        Seleciona as features (variáveis independentes) e a variável alvo para o modelo.
        
        Features selecionadas:
        - volatile acidity
        - density
        - alcohol
        - total sulfur dioxide
        - chlorides
        - sulphates
        
        Args:
            None
        
        Returns:
            tuple: Tupla contendo (X, y), onde X é o DataFrame de features e y é a Series da variável alvo.
        
        Raises:
            KeyError: Se alguma das colunas especificadas não existir no DataFrame.
        """
        if self.data is None:
            self.join_datasets()
        if self.y is None:
            self.apply_categoria()
        self.X = self.data[['volatile acidity', 'density', 'alcohol',
                            'total sulfur dioxide', 'chlorides', 'sulphates']]
        self.y = self.data['quality']
        return self.X, self.y

    def split_dados(self, test_size=0.2, random_state=42):
        """
        Divide os dados em conjuntos de treino e teste de forma estratificada.
        
        Args:
            test_size (float, opcional): Proporção dos dados destinados ao conjunto de teste. 
                Padrão é 0.2 (20% para teste, 80% para treino).
            random_state (int, opcional): Seed para reprodutibilidade da divisão aleatória. 
                Padrão é 42.
        
        Returns:
            tuple: Tupla contendo (X_train, X_test, y_train, y_test), os conjuntos de treino e teste.
        
        Raises:
            ValueError: Se test_size não estiver entre 0 e 1, ou se houver problemas com a estratificação.
        """
        if self.X is None or self.y is None:
            self.feature_selection()
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=test_size, random_state=random_state, stratify=self.y
        )
        return self.X_train, self.X_test, self.y_train, self.y_test

    def apply_model(self):
        """
        Treina o modelo de machine learning com os dados de treino.
        
        Args:
            None
        
        Returns:
            sklearn.base.BaseEstimator: Modelo treinado.
        
        Raises:
            ValueError: Se houver problemas com os dados de treino (ex: valores faltantes, tipos incompatíveis).
        """
        if self.X_train is None or self.y_train is None:
            self.split_dados()
        self.modelo.fit(self.X_train, self.y_train)
        return self.modelo

    def save_model(self, filepath=None):
        """
        Salva o modelo treinado em arquivo .joblib utilizando a biblioteca joblib.
        
        Se filepath não for fornecido, gera automaticamente o nome do arquivo
        baseado no tipo do modelo usado (ex: 'models/modelo_RandomForestClassifier.joblib').
        
        Args:
            filepath (str, opcional): Caminho do arquivo onde o modelo será salvo. 
                Se None, gera automaticamente baseado no tipo do modelo.
        
        Returns:
            None
        
        Raises:
            IOError: Se houver problemas ao escrever o arquivo no disco.
            PermissionError: Se não houver permissão de escrita no diretório especificado.
        """
        if filepath is None:
            model_name = type(self.modelo).__name__
            filepath = f'models/modelo_{model_name}.joblib'
        
        joblib.dump(self.modelo, filepath)
        print(f"Modelo salvo em: {filepath}")
    
    # def load_model(self, filepath):
    #     """
    #     Carrega um modelo previamente treinado e salvo em arquivo .joblib.
        
    #     Args:
    #         filepath (str): Caminho do arquivo .joblib contendo o modelo treinado.
        
    #     Returns:
    #         sklearn.base.BaseEstimator: Modelo carregado do arquivo.
        
    #     Raises:
    #         FileNotFoundError: Se o arquivo especificado não for encontrado.
    #         pickle.UnpicklingError: Se houver erro ao desserializar o arquivo .pkl.
    #     """
    #     self.modelo = joblib.load(filepath)
    #     print(f"Modelo carregado de: {filepath}")
    #     return self.modelo

    # def model_predict(self):
    #     """Realiza previsões."""
    #     if self.X_test is None:
    #         self.split_dados()
    #     return self.modelo.predict(self.X_test)

    def train(self):
        """
        Executa o pipeline completo de treinamento do modelo de ponta a ponta.
        
        O pipeline inclui:
        1. Leitura dos datasets de vinho tinto e branco
        2. Concatenação dos datasets
        3. Aplicação de categorização na variável qualidade
        4. Seleção de features
        5. Divisão de dados em treino e teste
        6. Treinamento do modelo
        7. Salvamento do modelo treinado
        
        Args:
            None
        
        Returns:
            None
        
        Raises:
            Exception: Qualquer exceção que possa ocorrer durante as etapas do pipeline.
        """
        self.leitura_dataset()
        self.join_datasets()
        self.apply_categoria()
        self.feature_selection()
        self.split_dados()
        self.apply_model()
        self.save_model()


# ---------------- Pipeline ----------------

# # Previsões
# y_pred = model.model_predict()
