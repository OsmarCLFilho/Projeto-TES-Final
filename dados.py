import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.use("Agg")

static_folder = "static"
original_csv_path = "data/data.csv"

target_col = "Target"

cols = [
    "Admission grade",
    "Age at enrollment",
    "Scholarship holder",
    target_col,
]


def csvUpload(path):
    #le o csv e separa por ";", tbm remove qualquer espaco ou tab escondida, caso tenha
    df = pd.read_csv(path, sep=";", encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    return df


def dataClear(df):
    #remocao do "Enrolled", duplicatas e ausencias
    df = df[df[target_col] != "Enrolled"].drop_duplicates()
    return df[cols].dropna()

def _colsTypes(df):
    #separacao das colunas, agora alem de somente numerica, ha tbm binarias e continuas
    numerics = df.select_dtypes(include="number")
    binarys = [c for c in numerics if numerics[c].nunique() == 2]
    continuous = [c for c in numerics if c not in binarys]

    return binarys, continuous


#comecando as estatisticas

#essa funcao é do que diz no slide 06, na parte analise do problema que é explicar tres achados do dataframe
def generateFindings(df):
    # multiplica por 100 para calcular porcentagem com .mean()
    givenUp = (df[target_col] == "Dropout") * 100

    scholarship = givenUp.groupby(df["Scholarship holder"]).mean().round(1)

    age = df.groupby(target_col)["Age at enrollment"].mean().round(1)
    grade = df.groupby(target_col)["Admission grade"].mean().round(1)

    return [
        f"Bolsistas desistem {scholarship[1]}%, contra {scholarship[0]}% dos nao bolsistas.",
        f"Idade media na matricula: {age['Dropout']} anos (desistencia) contra {age['Graduate']} (conclusao).",
        f"Nota de ingresso media: {grade['Dropout']} (desistencia) contra {grade['Graduate']} (conclusao).",
    ]


def _estatistics(brute):
    df = dataClear(brute)
    binarys, continuous = _colsTypes(df)
    givenUp = df[target_col] == "Dropout"
    stillIn = int((brute[target_col] == "Enrolled").sum())
    duplicates = int(brute.duplicated().sum())
    #total de celulas vazias (NaN) nas colunas usadas
    #(isna marca as vazias, sum soma por coluna, sum soma tudo)
    missing = int(brute[cols].isna().sum().sum())

    return {
        "linhas_antes": len(brute),
        "linhas_depois": len(df),
        "tipos": df.dtypes.astype(str).to_dict(),
        "amostra": df.head().to_dict(orient="records"),
        #Registro das transformacoe aplicadas em dataClear
        "transformacoes": [
            f"{stillIn} linhas 'Enrolled' removidas (aluno ainda matriculado, sem desfecho definido)",
            f"{duplicates} linhas duplicadas removidas",
            f"{missing} valores ausentes encontrados (linhas com ausentes sao removidas)",
            f"{brute.shape[1]} colunas reduzidas para as {df.shape[1]} usadas na analise",
        ],
        "descritivas": df[continuous].describe().round(2).to_dict(),
        "alvo": df[target_col].value_counts().to_dict(),
        #% de evasao para cada valor (0/1) de cada coluna binária
        "taxa_evasao": {c: (givenUp.groupby(df[c]).mean() * 100).round(1).to_dict() for c in binarys},
        "achados": generateFindings(df),
    }

def gerarEstatisticas():
    return _estatistics(csvUpload(original_csv_path))
 
 
def gerarEstatisticasCsv(df):
    return _estatistics(df)

#criando os graficos

def _save(fig, name):
    path = f"{static_folder}/name"
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return path

def _graphic(brute, sufix):
    df = dataClear(brute)
    binarys, _ = _colsTypes(df)

    #grafico de distribuicao: histograma nota ingresso
    fig, ax = plt.subplots()
    ax.hist(df["Admission grade"], bins=30)
    ax.set_title("Distribuicao de nota de ingresso")
    ax.set_xlabel("Nota de ingresso")
    ax.set_ylabel("Quantidade de alunos")
    distribution = _save(fig, f"GraficoDistribuicao{sufix}.png")

    #comparacao: taxa de desistencia por grupo, pelas colunas binarias

    #para cada coluna de 1 e 0, calcula a porcentagem de desistencia em cada valor, 
    #monta uma tabela com isso e a transpoe para o grafico agrupar as barras por coluna.
    #o T troca linhas por colunas
    taxas = pd.DataFrame({c: (df[target_col] == "Dropout").groupby(df[c]).mean() * 100 for c in binarys}).T

    fig, ax = plt.subplots()
    taxas.plot.bar(ax=ax, rot=0)
    ax.set_title("Taxa de desistencia por grupo")
    ax.set_xlabel("Grupo")
    ax.set_ylabel("Taxa de desistencia (%)")
    ax.legend(title="0 = Não / 1 = Sim")
    comparation = _save(fig, f"GraficoComparacao{sufix}.png")

    #Relacao: idade na matricula x nota de ingresso, separada pelo desfecho
    fig, ax = plt.subplots()
    for _class, group in df.groupby(target_col):
        ax.scatter(group["Age at enrollment"], group["Admission grade"], s=12, alpha=0.5, label=_class)
    ax.set_title("Relação entre idade na matrícula e nota de ingresso")
    ax.set_xlabel("Idade na matrícula")
    ax.set_ylabel("Nota de ingresso")
    ax.legend()
    relation = _save(fig, f"GraficoRelacao{sufix}.png")

    return {
        "graficoRelacao": relation,
        "graficoComparacao": comparation,
        "graficoDistribuicao": distribution,
    }
 
def gerarGraficos():
    return _graphic(csvUpload(original_csv_path), "Original")
 
def gerarGraficosCsv(df):
    return _graphic(df, "Csv")
 
if __name__ == "__main__":
    print(gerarEstatisticas())
    print(gerarGraficos())