import pandas as pd
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report


df = pd.read_csv('data/dataset.csv', sep=";")

df = df[df["Target"] != "Enrolled"]
print(df["Target"].value_counts())
print(df.shape)

##      nota de admissao    idade ao entrar     se possui bolsa
X = df[["Admission grade", "Age at enrollment", "Scholarship holder"]]
y = df["Target"]


X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.2, random_state=42
)

## -- Cria modelo
modelo = DecisionTreeClassifier(random_state=42)
## -- Treina
modelo.fit(X_treino, y_treino)

## -- Preve
previsoes = modelo.predict(X_teste)

## -- Compara previsao com dados corretos
acuracia = accuracy_score(y_teste, previsoes)
print("Acurácia:", acuracia)


## -- Mostra onde acertou e errou
matriz = confusion_matrix(y_teste, previsoes)

matriz_df = pd.DataFrame(
    matriz,
    index=["Era Dropout", "Era Graduate"],
    columns=["Previu Dropout", "Previu Graduate"]
)
print(matriz_df)

# Gera um relatório com métricas de avaliação do modelo,
# mostrando precisão, recall, F1-score e quantidade de exemplos por categoria.
print(classification_report(y_teste, previsoes))

plt.figure(figsize=(18, 10), dpi=150)

arvore = plot_tree(
    modelo,
    feature_names=["Nota de admissão", "Idade ao entrar", "Possui bolsa"],
    class_names=["Abandono", "Conclusão"],
    filled=True,
    max_depth=2, ## Limita a profundidade da visualização da árvore a 2 níveis.
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
plt.show()

# Salva o modelo treinado em um arquivo para utilizá-lo posteriormente no Flask.
joblib.dump(modelo, "modelo_decision_tree.pkl")