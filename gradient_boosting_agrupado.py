import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import warnings
from collections import Counter

caminho_tinto = '/media/babi/ssd/MESTRADO/PROJETO EM CD/wine+quality/winequality-red.csv'
caminho_branco = '/media/babi/ssd/MESTRADO/PROJETO EM CD/wine+quality/winequality-white.csv'

tinto = pd.read_csv(caminho_tinto, sep=';')
branco = pd.read_csv(caminho_branco,sep=';')
tinto['type'] = float(1)
branco['type'] = float(0)

df = pd.concat([tinto, branco], ignore_index=True) # a ordem dos dados no dataframe é estabelecida de acordo com a declarada
warnings.filterwarnings("ignore", category=FutureWarning)  
 

def agrupar_qualidade(qualidade):
    if qualidade <= 4:
        return 0  # Categoria "Ruim"
    elif qualidade <= 6:
        return 1  # Categoria "Médio"
    else: # qualidade >= 7
        return 2  # Categoria "Bom"

# Aplicar a função para criar a nova coluna alvo
df['quality_category'] = df['quality'].apply(agrupar_qualidade)

# Verificar a nova distribuição. Note como está MUITO mais balanceada!
print(f"Nova distribuição (agrupada):     {sorted(Counter(df['quality_category']).items())}")
print("-" * 40)



X = df.drop(['quality', 'quality_category'], axis=1)

# y é a nossa nova coluna com as 3 categorias
y = df['quality_category']


X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Treinamento do Modelo (sem SMOTE por enquanto) 

print("Treinando o modelo com as classes agrupadas...")
gb_classifier = GradientBoostingClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=3,
    random_state=42
)

gb_classifier.fit(X_train, y_train)
print("Modelo treinado com sucesso!")



y_pred = gb_classifier.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"\nAcurácia do modelo: {accuracy:.4f}")

print("\nRelatório de Classificação (Classes Agrupadas):")
target_names = ['Ruim (0)', 'Médio (1)', 'Bom (2)']
print(classification_report(y_test, y_pred, target_names=target_names))