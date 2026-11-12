import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import joblib
from dados import csvUpload, dataClear
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

os.makedirs("resultados", exist_ok=True)
# Carregar e tratar os dados
df = csvUpload("data/dataset.csv")
df = dataClear(df)

print(df["Target"].value_counts())
print(df.shape)

## Separar as variáveis de entrada e o resultado
X = df[["Admission grade", "Age at enrollment", "Scholarship holder"]]
y = df["Target"]

X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.2, random_state=404, stratify=y
)

## -- Cria modelo
modelo = DecisionTreeClassifier(random_state=404, max_depth=5)
## -- Treina
modelo.fit(X_treino, y_treino)

## -- Verifica a acurácia nos dados de treinamento
previsoes_treino = modelo.predict(X_treino)
acuracia_treino = accuracy_score(y_treino, previsoes_treino)

print("Acurácia no Treinamento:", acuracia_treino)

## -- Preve
previsoes = modelo.predict(X_teste)

## -- Compara previsao com dados corretos
acuracia = accuracy_score(y_teste, previsoes)
print("Acurácia:", acuracia)

## -- Calcula o baseline, utilizando a classe mais comum como previsão para todos os alunos.
classe_mais_comum = y_treino.value_counts().idxmax()
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

plt.savefig("resultados/decisiontree_confusao.png", dpi=300, bbox_inches="tight")

# Gera um relatório com métricas de avaliação do modelo,
# mostrando precisão, recall, F1-score e quantidade de exemplos por categoria.
print(classification_report(y_teste, previsoes))

plt.figure(figsize=(18, 10), dpi=150)

arvore = plot_tree(
    modelo,
    feature_names=["Nota de admissão", "Idade ao entrar", "Possui bolsa"],
    class_names=["Abandono", "Conclusão"],
    filled=True,
    max_depth=5, ## Limita a profundidade da visualização da árvore a 2 níveis.
    fontsize=10
)

# Traduz as informações exibidas nos blocos
for texto in plt.gca().texts:
    conteudo = texto.get_text()
    conteudo = conteudo.replace("gini", "Índice Gini")
    conteudo = conteudo.replace("samples", "Amostras")
    conteudo = conteudo.replace("value", "Quantidade")
    conteudo = conteudo.replace("class", "Classe")
    conteudo = conteudo.replace("True", "Sim")
    conteudo = conteudo.replace("False", "Não")
    texto.set_text(conteudo)

plt.tight_layout()
# Salvar imagem
plt.savefig("resultados/arvore_decisao.png", dpi=300, bbox_inches="tight")

# Salva o modelo treinado em um arquivo para utilizá-lo posteriormente no Flask.
joblib.dump(modelo, "modelo_decision_tree.pkl")
