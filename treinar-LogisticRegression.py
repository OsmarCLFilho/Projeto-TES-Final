import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from dados import dataClear

os.makedirs("resultados", exist_ok=True)
raw_df = pd.read_csv('data/dataset.csv', sep=";")

plt.switch_backend("TkAgg")

df = dataClear(raw_df)
print(df.loc[:, "Target"].value_counts())
print(df.shape)

##      nota de admissao    idade ao entrar     se possui bolsa
X = df[["Admission grade", "Age at enrollment", "Scholarship holder"]]
y = df["Target"]

X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.2, random_state=404, stratify=y
)

## -- Cria modelo
modelo = LogisticRegression(random_state=404)
## -- Treina
modelo.fit(X_treino, y_treino)

## -- Preve
previsoes = modelo.predict(X_teste)

## -- Compara previsao com dados corretos
acuracia = accuracy_score(y_teste, previsoes)
print("Acurácia:", acuracia)

## -- Calcula o baseline, utilizando a classe mais comum como previsão para todos os alunos.
classe_mais_comum = pd.Series(y_treino).value_counts().idxmax()
previsoes_baseline = [classe_mais_comum] * len(y_teste)
acuracia_baseline = accuracy_score(y_teste, previsoes_baseline)
print ("Acurácia do BaseLine: ", acuracia_baseline)

## -- Mostra onde acertou e errou
matriz = confusion_matrix(y_teste, previsoes)

matriz_df = pd.DataFrame(
    matriz,
    index=["Era Dropout", "Era Graduate"],
    columns=["Previu Dropout", "Previu Graduate"]
)


fig, ax = plt.subplots(figsize=(6, 5))

## -- Desenha a matriz de confusão
im = ax.imshow(matriz_df.values, cmap="Blues")
fig.colorbar(im, ax=ax, label="Count")

ax.set_xticks(np.arange(len(matriz_df.columns)))
ax.set_yticks(np.arange(len(matriz_df.index)), labels=matriz_df.index, rotation=45)
ax.set_xticklabels(matriz_df.columns)
ax.set_yticklabels(matriz_df.index)

threshold = matriz_df.values.max() / 2
for i in range(matriz_df.shape[0]):
    for j in range(matriz_df.shape[1]):
        valor = matriz_df.iloc[i, j]
        ax.text(
            j, i, f"{valor}",
            ha="center", va="center",
            fontsize=14,
            color="white" if valor > threshold else "black",
        )

ax.set_xlabel("Previsto")
ax.set_ylabel("Real")
ax.set_title("Matriz de Confusão")

plt.tight_layout()

plt.savefig("resultados/logistico_confusao.png", dpi=300, bbox_inches="tight")
plt.show()

# Gera um relatório com métricas de avaliação do modelo,
# mostrando precisão, recall, F1-score e quantidade de exemplos por categoria.
print(classification_report(y_teste, previsoes))

# Salva o modelo treinado em um arquivo para utilizá-lo posteriormente no Flask.
joblib.dump(modelo, "modelo_logistico.pkl")
