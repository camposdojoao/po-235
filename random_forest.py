# Bibliotecas
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Desenvolvimento do modelo
class Modelo:
    def __init__(self, path_wine_red, path_wine_white, modelo):
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
        """Lê os CSVs de vinho tinto e branco."""
        self.df_red = pd.read_csv(self.path_wine_red, sep=';')
        self.df_white = pd.read_csv(self.path_wine_white, sep=';')
        return self.df_red, self.df_white

    def join_datasets(self):
        """Concatena os datasets em um único DataFrame."""
        if self.df_red is None or self.df_white is None:
            self.leitura_dataset()
        self.data = pd.concat([self.df_red, self.df_white], ignore_index=True)
        return self.data

    def apply_categoria(self):
        """Converte 'quality' em categorias: Boa, Média ou Ruim."""
        if self.data is None:
            self.join_datasets()
        self.data['quality'] = self.data['quality'].apply(
            lambda q: 'Boa' if q >= 7 else ('Média' if q > 5 else 'Ruim')
        )
        self.y = self.data['quality']
        return self.y

    def feature_selection(self):
        """Seleciona as features e o alvo."""
        if self.data is None:
            self.join_datasets()
        if self.y is None:
            self.apply_categoria()
        self.X = self.data[['volatile acidity', 'density', 'alcohol',
                            'total sulfur dioxide', 'chlorides', 'sulphates']]
        self.y = self.data['quality']
        return self.X, self.y

    def split_dados(self, test_size=0.2, random_state=42):
        """Divide os dados em treino e teste."""
        if self.X is None or self.y is None:
            self.feature_selection()
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=test_size, random_state=random_state, stratify=self.y
        )
        return self.X_train, self.X_test, self.y_train, self.y_test

    def apply_model(self):
        """Treina o modelo."""
        if self.X_train is None or self.y_train is None:
            self.split_dados()
        self.modelo.fit(self.X_train, self.y_train)
        return self.modelo

    def model_predict(self):
        """Realiza previsões."""
        if self.X_test is None:
            self.split_dados()
        return self.modelo.predict(self.X_test)


# ---------------- Pipeline ----------------
model = Modelo(
    '/home/lucasmoreira/Downloads/Data Science Project/po-235/src/winequality-red.csv',
    '/home/lucasmoreira/Downloads/Data Science Project/po-235/src/winequality-white.csv',
    RandomForestClassifier(random_state=42)
)

# Execução
model.leitura_dataset()
model.join_datasets()
model.apply_categoria()
model.feature_selection()
model.split_dados()
model.apply_model()

# Previsões
y_pred = model.model_predict()

# Avaliação
print(f"Acurácia: {accuracy_score(model.y_test, y_pred) * 100:.2f} %\n")
print("Relatório de Classificação:")
print(classification_report(model.y_test, y_pred, digits=3))
