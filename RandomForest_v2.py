### ------- SEM SMOTE --------------

# Bibliotecas
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Leitura dos dados
df_red = pd.read_csv("/home/lucasmoreira/Downloads/Data Science Project/po-235/src/winequality-red.csv", sep=';')
df_white = pd.read_csv("/home/lucasmoreira/Downloads/Data Science Project/po-235/src/winequality-white.csv", sep=';')

# Criando a coluna labels em ambos os dataframe pandas
df_red['labels'] = 0
df_white['labels'] = 1

# Concatenando os dados
data = pd.concat([df_red, df_white], ignore_index=True)

# Features
#X = data[['fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar',
#          'chlorides', 'free sulfur dioxide', 'total sulfur dioxide', 'density',
 #         'pH', 'sulphates', 'alcohol']]

X = data[['volatile acidity', 'density', 'alcohol','total sulfur dioxide',
          'chlorides','sulphates']]

# Criando categoria
def categoria_quality(q):

    if q >= 7:
        return "Boa"
    
    elif 5 < q < 7:
        return "Média"
    
    else:
        return "Ruim"

# Definindo as categorias: Boa, Média e Ruim
y = data['quality'].apply(categoria_quality)

# Divisão treino/teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Treinamento do modelo
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Predição
y_pred = model.predict(X_test)

# Avaliação
print(f"Acurácia: {accuracy_score(y_test, y_pred) * 100:.2f} %\n")
print("Relatório de Classificação:")
print(classification_report(y_test, y_pred, digits=3))


### ------- COM SMOTE --------------

# SMOTE
from imblearn.over_sampling import SMOTE

# Aplicando o smote
smote = SMOTE(random_state=42, k_neighbors=2)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

# Testando um novo modelo
model_v2 = RandomForestClassifier(random_state=42)
model_v2.fit(X_train_res, y_train_res)

# Nova avaliação
y_pred_v2 = model_v2.predict(X_test)
print(f"Acurácia: {accuracy_score(y_test, y_pred_v2) * 100:.2f} %\n")
print("Relatório de Classificação:")
print(classification_report(y_test, y_pred_v2, digits=3))

