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
        colunas_necessarias = ["Admission grade", "Age at enrollment", "Scholarship holder"]
        if not all(col in dataframe.columns for col in colunas_necessarias):
            return render_template(
                'form.html',
                erro="O CSV deve conter as colunas: 'Admission grade', 'Age at enrollment' e 'Scholarship holder'."
            )
        X = dataframe[colunas_necessarias].dropna()
        if X.empty:
            return render_template('form.html', erro="O arquivo CSV não possui linhas válidas para previsão.")
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
        dataframe = pd.DataFrame([{
            "Admission grade": float(data.get("admission_grade", "")),
            "Age at enrollment": int(data.get("age_at_enrollment", "")),
            "Scholarship holder": int(data.get("scholarship_holder", ""))
        }])
    except (ValueError, TypeError):
        return render_template('form.html', erro="Preencha todos os campos do formulário com valores válidos.")

    previsaoLogistico = modeloLogistico.predict(dataframe)
    previsaoDecision = modeloDecision.predict(dataframe)

    return render_template('previsao.html', resultadoLog = previsaoLogistico[0], resultadoDes = previsaoDecision[0])

if __name__ == "__main__":
    app.run(debug=True)