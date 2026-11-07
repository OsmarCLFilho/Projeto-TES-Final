from flask import Flask, render_template, url_for, request, redirect
import random
import os

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def getHome():
    return render_template('index.html')

@app.route("/form")
def formEnvio():
    return render_template('form.html')

@app.post("/previsaoCsv")
def preverResultadoCsv():
    if 'arquivo' not in request.files:
        return redirect(url_for('formEnvio'))

    arquivo = request.files['arquivo']

    if(arquivo.filename == ''):
        return redirect(url_for('formEnvio'))

    if arquivo and not arquivo.filename.split('.')[1] == 'csv':
        return redirect(url_for('formEnvio'))
    
    arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], arquivo.filename))

    #Chamar a função de gerar graficos passando o caminho do arquivo

    #Chamar a função de prever resultados passando o caminho do arquivo
    previsoes = []
    for i in range(random.randrange(100, 1000)):
        previsoes.append({
            "id": i,
            "result": random.randint(0,1)
        })

    dados = {
        "graficoRelacao": "/graficoRelacaoCsv",
        "graficoComparacao": "/graficoComparacaoCsv",
        "graficoDistribuicao": "/graficoDistribuicaoCsv",
        "previsoes": previsoes
    }

    return render_template('previsaoCsv.html', dados = dados)

@app.post("/previsao")
def preverResultados():
    resultado = random.randint(0, 1)
    return render_template('previsao.html', resultado = resultado)

app.run(debug=True)