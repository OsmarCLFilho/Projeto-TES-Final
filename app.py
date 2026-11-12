from flask import Flask, render_template, url_for, request, redirect
import random
import os
import pandas as pd
import joblib 
import dados

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

modeloLogistico = joblib.load("./modelo_logistico.pkl")
modeloDecision = joblib.load("./modelo_decision_tree.pkl")

@app.route("/")
def getHome():
    return render_template('index.html')

@app.route("/form")
def formEnvio():
    return render_template('form.html')

@app.post("/previsaoCsv")
def preverResultadoCsv():
    if 'arquivo' not in request.files:
        return render_template('form.html', erro="Nenhum arquivo foi enviado.")

    arquivo = request.files['arquivo']

    if arquivo.filename == '':
        return render_template('form.html', erro="Por favor, selecione um arquivo CSV.")

    if not arquivo.filename.lower().endswith('.csv'):
        return render_template('form.html', erro="Formato inválido. Envie apenas arquivos com extensão .csv.")

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], arquivo.filename)
    arquivo.save(caminho_arquivo)

    try:
        dataframe = pd.read_csv(caminho_arquivo, sep=None, engine='python')
        dataframe.columns = dataframe.columns.str.strip()
        colunas_necessarias = ["Admission grade", "Age at enrollment", "Scholarship holder"]
        if not all(col in dataframe.columns for col in colunas_necessarias):
            return render_template(
                'form.html',
                erro="O CSV deve conter as colunas: 'Admission grade', 'Age at enrollment' e 'Scholarship holder'."
            )
        X = dataframe[colunas_necessarias].dropna().copy()
        if X.empty:
            return render_template('form.html', erro="O arquivo CSV não possui linhas válidas para previsão.")

        for col in colunas_necessarias:
            X[col] = pd.to_numeric(X[col], errors='coerce')

        if X.isna().any().any():
            return render_template(
                'form.html',
                erro="O CSV contém valores incompatíveis (texto ou formato inválido onde são esperados números)."
            )

        notas_invalidas = (X["Admission grade"] < 0) | (X["Admission grade"] > 200)
        idades_invalidas = (X["Age at enrollment"] < 14) | (X["Age at enrollment"] > 100) | (X["Age at enrollment"] % 1 != 0)
        bolsas_invalidas = ~X["Scholarship holder"].isin([0, 1])

        if notas_invalidas.any() or idades_invalidas.any() or bolsas_invalidas.any():
            return render_template(
                'form.html',
                erro="O CSV contém valores impossíveis: 'Admission grade' deve estar entre 0 e 200, 'Age at enrollment' inteiro entre 14 e 100, e 'Scholarship holder' deve ser 0 ou 1."
            )

        X["Age at enrollment"] = X["Age at enrollment"].astype(int)
        X["Scholarship holder"] = X["Scholarship holder"].astype(int)
    except Exception:
        return render_template('form.html', erro="Erro ao ler o arquivo CSV. Verifique se o arquivo está formatado corretamente.")
    

    previsaoLogistico = modeloLogistico.predict(X)
    previsaoDecision = modeloDecision.predict(X)

    dfLog = X.copy()
    dfLog["Target"] = previsaoLogistico

    dfDes = X.copy()
    dfDes["Target"] = previsaoDecision

    graficosLog = dados.gerarGraficosCsv(dfLog, "Logistico")
    graficosDes = dados.gerarGraficosCsv(dfDes, "Decision")

    estatisticasOriginal = dados.gerarEstatisticas()
    estatisticasLog = dados.gerarEstatisticasCsv(dfLog)
    estatisticasDes = dados.gerarEstatisticasCsv(dfDes)

    return render_template(
        'previsaoCsv.html',
        previsaoDes=previsaoDecision,
        previsaoLog=previsaoLogistico,
        graficosLog=graficosLog,
        graficosDes=graficosDes,
        estatisticasOriginal=estatisticasOriginal,
        estatisticasLog=estatisticasLog,
        estatisticasDes=estatisticasDes,
    )

@app.post("/previsao")
def preverResultados():

    data = request.form
    print(data)
        
    if not data:
        return render_template('form.html', erro="Nenhum dado do formulário foi recebido.")

    try:
        nota = float(data.get("admission_grade", ""))
        idade = int(data.get("age_at_enrollment", ""))
        bolsa = int(data.get("scholarship_holder", ""))
    except (ValueError, TypeError):
        return render_template('form.html', erro="Preencha todos os campos do formulário com valores válidos.")

    if not (0 <= nota <= 200) or not (14 <= idade <= 100) or bolsa not in (0, 1):
        return render_template(
            'form.html',
            erro="Valores fora do limite permitido: Nota deve ser de 0 a 200, Idade de 14 a 100 e Condição de Bolsista 0 ou 1."
        )

    dataframe = pd.DataFrame([{
        "Admission grade": nota,
        "Age at enrollment": idade,
        "Scholarship holder": bolsa
    }])

    previsaoLogistico = modeloLogistico.predict(dataframe)
    previsaoDecision = modeloDecision.predict(dataframe)

    return render_template('previsao.html', resultadoLog = previsaoLogistico[0], resultadoDes = previsaoDecision[0])

if __name__ == "__main__":
    app.run(debug=True)