"""Previsão da Qualidade de Vinhos com XGBoost e SMOTE

Objetivo: Construir um modelo de Machine Learning para prever a nota de qualidade
de um vinho (3 a 9) com base em características físico-químicas. SMOTE é usado para
lidar com o desbalanceamento das classes de qualidade.
"""


# Importa a biblioteca pandas para manipulação de dados
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # backend non-interactive (safe for CI / headless)

# Carrega os dois arquivos .csv a partir do diretório local `src/`.
from pathlib import Path
base_dir = Path(__file__).resolve().parents[1]  # repo root -> tests/.. -> project root
csv_dir = base_dir / 'src'

# garante que o diretório de resultados exista (para salvar gráficos)
Path(base_dir / 'resultados').mkdir(parents=True, exist_ok=True)

# O 'sep=';' indica que o separador de colunas é o ponto-e-vírgula.
df_red = pd.read_csv(csv_dir / 'winequality-red.csv', sep=';')
df_white = pd.read_csv(csv_dir / 'winequality-white.csv', sep=';')

# Adiciona a coluna 'labels' para criar nosso alvo (target)
# 0 = Vinho Tinto
df_red['labels'] = 0
# 1 = Vinho Branco
df_white['labels'] = 1

# Junta as duas tabelas em um único DataFrame chamado 'data'
data = pd.concat([df_red, df_white], ignore_index=True)

# Exibe as 5 primeiras linhas para confirmar que a junção funcionou
print("Amostra do dataset unificado:")
print(data.head().to_string())

## Análise da Variável Alvo (Balanceamento da 'quality')

# Ver quantas amostras temos de cada nota de qualidade.

import matplotlib.pyplot as plt
import seaborn as sns

print("Contagem de vinhos por nota de qualidade:")
print(data['quality'].value_counts().sort_index()) # .sort_index() para ordenar as notas

# Gerando um gráfico para a apresentação visual

plt.figure(figsize=(10, 6)) # Aumenta o tamanho do gráfico para melhor visualização
sns.countplot(x='quality', data=data, palette='viridis')
plt.title('Distribuição das Notas de Qualidade do Vinho', fontsize=16)
plt.xlabel('Qualidade', fontsize=12)
plt.ylabel('Contagem', fontsize=12)
# salvar figura (ambientes headless / CI)
plt.savefig(base_dir / 'resultados' / 'quality_distribution.png', bbox_inches='tight')
plt.clf()

"**Conclusão da Análise:** A análise confirma que as notas de qualidade são **desbalanceadas**. "
"As notas medianas (5 e 6) dominam o dataset, enquanto as notas extremas são muito raras. "
"Isso justifica a aplicação da técnica SMOTE para que o modelo aprenda a reconhecer também os vinhos de qualidade rara, e não apenas os vinhos medianos."

## Modelagem com XGBoost sem Balanceamento

# ===================================================================
# TREINAMENTO NO DATASET ORIGINAL (DESBALANCEADO)
# ===================================================================

# --- Importação das bibliotecas (só para garantir que a célula rode de forma independente) ---

import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder # Importando LabelEncoder

print("--- Iniciando Treinamento SEM SMOTE (Previsão de QUALIDADE) ---")

# --- Preparação das variáveis para o modelo ---
# X (maiúsculo) = Features (características que usamos para prever)
# Estamos removendo APENAS 'quality', pois 'labels' (tinto/branco) é uma feature útil!
X = data.drop('quality', axis=1)
# y (minúsculo) = Target (o que queremos prever)
# Agora nosso alvo é a QUALIDADE.
y = data['quality']

# --- Codificação das classes para o XGBoost ---
# XGBoost espera classes começando de 0.
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# --- Divisão em Treino e Teste ---
# Dividimos os dados: 80% para treinar, 20% para testar.
# 'stratify=y_encoded' mantém a proporção das notas de qualidade nos dois conjuntos (importante mesmo sem SMOTE no treino).
X_train, X_test, y_train_encoded, y_test_encoded = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)
print(f"Dados de treino: {len(X_train)} vinhos | Dados de teste: {len(X_test)} vinhos")

# --- Criação de um NOVO Modelo XGBoost ---
# É uma boa prática criar uma nova variável para o modelo para não sobrescrever o anterior.
# Vamos chamá-lo de 'model_desbalanceado'.
model_desbalanceado = xgb.XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42)


# --- Treinamento do Modelo nos Dados Originais ---
# A MUDANÇA PRINCIPAL ESTÁ AQUI!
# Note que usamos 'X_train' e 'y_train_encoded', e NÃO 'X_train_smote' e 'y_train_smote'.
# Estamos ensinando o modelo com os dados exatamente como eles são, com o desbalanceamento de QUALIDADE.
model_desbalanceado.fit(X_train, y_train_encoded) # Usando y_train_encoded

print("\nModelo XGBoost (desbalanceado, prevendo QUALIDADE) treinado com sucesso!")


# --- Avaliação do Modelo Desbalanceado ---
# Fazemos as previsões no mesmo conjunto de teste de antes para uma comparação justa.
y_pred_encoded = model_desbalanceado.predict(X_test) # As previsões também estarão codificadas

print("\n--- Resultados Finais da Avaliação (SEM SMOTE, prevendo QUALIDADE) ---")
print("\nRelatório de Classificação:")
# Precisamos decodificar os rótulos de volta para as notas originais para o classification_report
print(classification_report(le.inverse_transform(y_test_encoded), le.inverse_transform(y_pred_encoded)))

"""## Modelagem com XGBoost e SMOTE
---

Agora, vamos construir nosso modelo para prever a **qualidade**. O processo é o mesmo de antes, mas com o alvo e as features ajustadas para o nosso novo objetivo.
"""

# --- Importação das bibliotecas para a modelagem ---
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import LabelEncoder

# --- Preparação das variáveis para o modelo ---
# X = Features. Agora removemos APENAS 'quality', pois 'labels' (tinto/branco) é uma feature útil!
X = data.drop('quality', axis=1)
# y = Target. Nosso novo alvo é a coluna 'quality'.
y = data['quality']

# --- Codificação das classes para o XGBoost ---
# XGBoost espera classes começando de 0.
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# --- Divisão em Treino e Teste ---
# 'stratify=y_encoded' é ainda mais importante aqui, para manter a proporção das raras notas de qualidade.
X_train, X_test, y_train_encoded, y_test_encoded = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)
print("--- Iniciando a etapa de modelagem ---")
print(f"Dados de treino: {len(X_train)} vinhos | Dados de teste: {len(X_test)} vinhos")


# --- Aplicação do SMOTE (Apenas no Treino!) ---
# O SMOTE agora vai criar amostras sintéticas das notas de qualidade raras (3, 4, 8, 9)
# para que todas as classes tenham o mesmo número de amostras que a classe majoritária no treino.
# Setting k_neighbors to 3 to handle the smallest class size
def safe_smote_resample(X_train, y_train, random_state=42, desired_k=3):
	"""Apply SMOTE safely: choose k_neighbors based on smallest class size.

	If smallest class has <=1 sample, fall back to original data (no resampling).
	"""
	from collections import Counter
	counts = Counter(y_train)
	min_count = min(counts.values())
	if min_count <= 1:
		# Not enough samples to perform SMOTE
		return X_train, y_train
	k = min(desired_k, max(1, min_count - 1))
	sm = SMOTE(random_state=random_state, k_neighbors=k)
	return sm.fit_resample(X_train, y_train)


smote = SMOTE(random_state=42, k_neighbors=3)
X_train_smote, y_train_smote_encoded = safe_smote_resample(X_train, y_train_encoded, random_state=42, desired_k=3)
print("\nDistribuição das notas de qualidade no treino DEPOIS do SMOTE (codificadas):")
print(pd.Series(y_train_smote_encoded).value_counts().sort_index())


# --- Treinamento do Modelo XGBoost ---
# O XGBoost é ótimo para problemas multi-classe como este.
# O treinamento é feito nos dados de treino balanceados.
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42)
model.fit(X_train_smote, y_train_smote_encoded)
print("\nModelo XGBoost treinado com sucesso!")


# --- Avaliação do Modelo ---
# Fazemos as previsões no conjunto de teste original (desbalanceado).
# Salva as previsões do modelo COM SMOTE em uma variável diferente para evitar sobrescrever
y_pred_encoded_smote = model.predict(X_test)

print("\n--- Resultados Finais da Avaliação ---")
print("\nRelatório de Classificação (prevendo a QUALIDADE):")
# O relatório agora mostrará a performance para cada nota de qualidade.
# É normal que a performance seja menor para as notas raras (3, 4, 8, 9).
# Precisamos decodificar as previsões e os rótulos de teste para o classification_report
print(classification_report(le.inverse_transform(y_test_encoded), le.inverse_transform(y_pred_encoded_smote)))

## 4. Conclusão

"O relatório de classificação mostra que o modelo tem uma boa performance geral, especialmente na identificação das classes mais comuns (notas 5 e 6)." 
"Prever as notas extremas (como 3 ou 9) é um desafio muito maior devido à sua raridade, mas o uso de SMOTE permitiu que o modelo ao menos aprendesse a reconhecer algumas dessas amostras, o que não seria possível sem o rebalanceamento."

## Análise Comparativa Extra:

##### Classes Majoritárias (5 e 6):
#A performance é similar nos dois modelos. Isso é esperado, pois essas classes são abundantes e em termos de precision, recall e F1-score para as classes 5 e 6 é bastante sio modelo consegue aprender bem com elas mesmo sem SMOTE."

#A acurácia geral (accuracy) é ligeiramente maior no modelo sem SMOTE (0.67 vs 0.62), o que pode acontecer porque ele se concentra mais em acertar as classes majoritárias."

###### Classes Minoritárias (3, 4, 7, 8, 9): É aqui que vemos o impacto do SMOTE:

#Classes 3 e 9: Ambos os modelos falham completamente em prever as classes 3 e 9 (precision, recall e f1-score de 0.00). Isso ocorre porque o número de amostras dessas classes no conjunto de teste (support) é extremamente baixo (6 para a classe 3 e apenas 1 para a classe 9). Mesmo com SMOTE, é muito difícil para o modelo generalizar e prever corretamente classes com tão poucas amostras no conjunto de teste real."

#Classe 4: O modelo COM SMOTE teve um recall e F1-score melhores para a classe 4 (0.23 e 0.23) comparado ao modelo SEM SMOTE (0.09 e 0.13). Isso indica que o SMOTE ajudou o modelo a identificar uma proporção maior dos vinhos de qualidade 4."

#Classe 8: Similarmente, o modelo COM SMOTE teve um recall ligeiramente melhor para a classe 8 (0.36 vs 0.36 - neste caso específico, os recalls foram iguais, o que é interessante, mas o F1-score é menor para o modelo COM SMOTE (0.33 vs 0.51)). Isso pode variar em diferentes execuções, mas a intenção do SMOTE é melhorar a capacidade de identificação (recall) das classes minoritárias. O F1-score combina precision e recall, e a queda na precision para a classe 8 no modelo COM SMOTE pode ter impactado o F1-score.

#Classe 7: O modelo COM SMOTE teve um recall melhor (0.62 vs 0.61) mas um precision e F1-score ligeiramente menores (0.56 e 0.59 vs 0.63 e 0.62) para a classe 7. O SMOTE pode levar a um aumento nos falsos positivos para a classe minoritária (diminuindo a precision) enquanto aumenta os verdadeiros positivos (aumentando o recall).

#Macro Avg vs Weighted Avg:

#macro avg (média simples das métricas por classe): As métricas macro avg são mais baixas no modelo COM SMOTE (0.35 F1-score) comparado ao modelo SEM SMOTE (0.38 F1-score). Isso porque o macro avg dá o mesmo peso para todas as classes, incluindo as minoritárias onde a performance ainda é desafiadora. O SMOTE melhora as métricas das minoritárias, mas não o suficiente para superar a dificuldade inerente de prever classes raras no teste.

#weighted avg (média ponderada pelo número de amostras por classe): As métricas weighted avg são mais altas em ambos os modelos (0.62 e 0.66 F1-score) porque dão mais peso às classes majoritárias (5 e 6), onde o modelo se sai melhor. O modelo SEM SMOTE tem um weighted avg ligeiramente maior, refletindo sua maior acurácia geral focada nas classes mais comuns.

#Conclusão:

#O SMOTE não fez milagres para as classes extremamente raras (3 e 9) devido ao seu baixíssimo suporte no conjunto de teste. No entanto, ele demonstrou um benefício claro ao melhorar o recall e o F1-score para classes minoritárias um pouco maiores, como a classe 4. Isso mostra que o SMOTE ajudou o modelo a se tornar um pouco menos enviesado para as classes majoritárias e a ser capaz de identificar corretamente mais amostras das classes menos frequentes, mesmo que a acurácia geral possa diminuir um pouco em favor de uma melhor performance nas classes minoritárias.

#Prever a qualidade do vinho com este dataset continua sendo um desafio significativo devido ao forte desbalanceamento das notas. O SMOTE é uma ferramenta útil para mitigar esse problema, mas não elimina completamente a dificuldade de prever classes com pouquíssimas amostras."

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import numpy as np

# Gerando a matriz de confusão para o modelo SEM SMOTE
# Usamos os resultados (y_test_encoded e y_pred_encoded) da célula TOZWDm7B6THK
# Note que y_test_encoded e y_pred_encoded são do modelo SEM SMOTE nesta célula
cm_desbalanceado = confusion_matrix(le.inverse_transform(y_test_encoded), le.inverse_transform(y_pred_encoded))

# Exibindo a matriz de confusão
# Usamos os rótulos originais de qualidade para exibição
quality_labels = np.sort(data['quality'].unique())
disp_desbalanceado = ConfusionMatrixDisplay(confusion_matrix=cm_desbalanceado, display_labels=quality_labels)

fig, ax = plt.subplots(figsize=(10, 10)) # Ajusta o tamanho da figura para melhor legibilidade
disp_desbalanceado.plot(cmap=plt.cm.Blues, ax=ax)
plt.title('Matriz de Confusão para Previsão de Qualidade (SEM SMOTE)', fontsize=16)
plt.xlabel('Rótulo Predito', fontsize=12)
plt.ylabel('Rótulo Verdadeiro', fontsize=12)
# Save figure instead of show() so script works headless
plt.savefig('resultados/confusion_matrix_desbalanceado.png', bbox_inches='tight')

print("\nMatriz de Confusão (SEM SMOTE):")
print(cm_desbalanceado)

## Comparativo das Matrizes de Confusão (Previsão de Qualidade)

## **Análise Visual:**

#*   **Diagonal Principal:** Os números na diagonal principal representam as previsões corretas (Verdadeiros Positivos para cada classe). Compare esses números entre as duas matrizes. Geralmente, esperamos que o modelo COM SMOTE tenha números maiores na diagonal para as classes minoritárias (embora isso possa variar dependendo da classe).
#*   **Fora da Diagonal Principal:** Os números fora da diagonal principal representam os erros de classificação (Falsos Positivos e Falsos Negativos). Observe como os erros estão distribuídos em cada matriz.
#    *   **Falsos Negativos (FN):** Olhe para as linhas. Por exemplo, na linha do True Label 4, os números fora da diagonal mostram quantas amostras de qualidade 4 foram classificadas incorretamente como outras qualidades. Compare esses números para a classe 4 entre os dois modelos. Um modelo melhor para classes minoritárias deve ter menos FNs para essas classes.
 #   *   **Falsos Positivos (FP):** Olhe para as colunas. Por exemplo, na coluna do Predicted Label 4, os números fora da diagonal mostram quantas amostras de outras qualidades foram classificadas incorretamente como qualidade 4. O SMOTE, ao aumentar a sensibilidade às classes minoritárias, às vezes pode aumentar os FPs para essas classes.

#**Pontos Chave para Observar:**

#*   Quão bem cada modelo previu as classes majoritárias (5 e 6)?
#*   Qual modelo teve menos erros (FNs) ao tentar identificar as classes minoritárias (3, 4, 7, 8, 9)?
#*   O aumento do recall nas classes minoritárias no modelo COM SMOTE veio acompanhado de um aumento significativo nos falsos positivos para essas classes (diminuindo a precisão)?

# A matriz de confusão é uma ótima ferramenta visual para entender onde cada modelo está acertando e errando, e como o SMOTE alterou o comportamento do modelo em relação às diferentes classes de qualidade.

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import numpy as np

# Gerando a matriz de confusão para o modelo COM SMOTE
# Usamos os resultados (y_test_encoded e y_pred_encoded) da célula 0KN6rfBuuV4K
cm_smote = confusion_matrix(le.inverse_transform(y_test_encoded), le.inverse_transform(y_pred_encoded_smote))

# Exibindo a matriz de confusão
# Usamos os rótulos originais de qualidade para exibição
quality_labels = np.sort(data['quality'].unique())
disp_smote = ConfusionMatrixDisplay(confusion_matrix=cm_smote, display_labels=quality_labels)

fig, ax = plt.subplots(figsize=(10, 10)) # Ajusta o tamanho da figura para melhor legibilidade
disp_smote.plot(cmap=plt.cm.Blues, ax=ax)
plt.title('Matriz de Confusão para Previsão de Qualidade (COM SMOTE)', fontsize=16)
plt.xlabel('Rótulo Predito', fontsize=12)
plt.ylabel('Rótulo Verdadeiro', fontsize=12)
plt.savefig('resultados/confusion_matrix_smote.png', bbox_inches='tight')

print("\nMatriz de Confusão (COM SMOTE):")
print(cm_smote)

from sklearn.metrics import accuracy_score

# Calculando a acurácia do modelo SEM SMOTE
# No script acima as variáveis codificadas são: y_test_encoded e y_pred_encoded (modelo sem SMOTE).
# Decodificamos para as labels originais antes de calcular a acurácia.
try:
	y_test_orig = le.inverse_transform(y_test_encoded)
	y_pred_orig_desbalanceado = le.inverse_transform(y_pred_encoded)
	accuracy_desbalanceado = accuracy_score(y_test_orig, y_pred_orig_desbalanceado)
	print(f"Acurácia do modelo SEM SMOTE (Previsão de Qualidade): {accuracy_desbalanceado:.4f}")
except Exception:
	print("Não foi possível calcular a acurácia (variáveis esperadas não encontradas). Certifique-se de que os passos anteriores foram executados com sucesso.")


def main():
	# This script was converted from a Colab notebook; main execution is the
	# top-level flow that already ran when imported. We expose a main() so
	# it can be invoked programmatically or extended later.
	pass


if __name__ == "__main__":
	# ensure resultados directory exists for saving plots
	from pathlib import Path
	Path('resultados').mkdir(parents=True, exist_ok=True)
	main()