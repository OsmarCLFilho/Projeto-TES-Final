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
    #separacao das colunas, agora alem de somente numeria, ha tbm binarias e continuas
    numerics = df.select_dtypes(include="number")
    binarys = [c for c in numerics if numerics[c].nunique() == 2]
    continuous = [c for c in numerics if c not in binarys]

    return binarys, continuous


#comecando as estatisticas

#essa funcao eh do que diz no slide 06, na parte analise do problema que eh explicar tres achados do dataframe
def generateFindings(df):
    givenUp = (df[target_col] == "Dropout") * 100 #se der 100, eh pq desistiu, o 0 se concluiu
    scholarship = givenUp.groupby(df["Scholarship holder"]).mean().round(1)
    age = df.groupby(target_col)["Age at enrollment"].mean().round(1)
    nota = df.groupby(target_col)["Admission grade"].mean().round(1)

    return [
        f"Bolsistas desistem {bolsa[1]}%, contra {bolsa[0]}% dos nao bolsistas.",
        f"Idade media na matricula: {idade['Dropout']} anos (desistencia) contra {idade['Graduate']} (conclusao).",
        f"Nota de ingresso media: {nota['Dropout']} (desistencia) contra {nota['Graduate']} (conclusao).",
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
        # % de evasão para cada valor (0/1) de cada coluna binária
        "taxa_evasao": {c: (givenUp.groupby(df[c]).mean() * 100).round(1).to_dict() for c in binarys},
        "achados": generateFindings(df),
    }

def gerarEstatisticas():
    return _estatistics(csvUpload(original_csv_path))
 
 
def gerarEstatisticasCsv(df):
    return _estatistics(df)

#comecando os graficos

def _save(fig, name):
    path = f"{static_folder}/name"
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return path

def _graphic(brute, sufix):
    df = dataClear(brute)
    binarys, _ = _colsTypes(df)

    

    

