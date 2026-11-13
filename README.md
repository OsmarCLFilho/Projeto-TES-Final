# Eai, vai trancar? — Previsão de evasão universitária

Trabalho Final de **Tópicos Especiais em Software**.
Aplicação web em Flask que analisa dados de estudantes com Pandas, gera gráficos e prevê **evasão ou conclusão** do curso com modelos de aprendizado supervisionado (scikit-learn)

Link para acesso ao repositório: https://github.com/OsmarCLFilho/Projeto-TES-Final.

## Participação de cada integrante

| Integrante | Responsabilidades |
|---|---|
| João Pellison | Árvore de Decisão (treino, avaliação e relatório) |
| Matheus Camilo | Limpeza, estatísticas e gráficos com base no dataset do tema |
| Osmar Cardoso | Regressão Logística (treino, avaliação e relatório), revisão e integração |
| Pedro Volpatto | Aplicação Flask, validações, templates HTML e estilo |

## Sumário

1. [Pergunta do projeto](#1-pergunta-do-projeto)
2. [Dataset](#2-dataset)
3. [Instalação e execução](#3-instalação-e-execução)
4. [Estrutura do projeto](#4-estrutura-do-projeto)
5. [Esquema do CSV aceito](#5-esquema-do-csv-aceito)
6. [Tratamento e análise dos dados](#6-tratamento-e-análise-dos-dados)
7. [Variáveis X e y](#7-variáveis-x-e-y)
8. [Modelos testados e comparação](#8-modelos-testados-e-comparação)
9. [Escolha final do modelo](#9-escolha-final-do-modelo)
10. [Integração com o Flask](#10-integração-com-o-flask)
11. [Limitações](#11-limitações)
12. [Fontes, ferramentas e uso de IA](#12-ferramentas-utilizadas)

---

## 1. Pergunta do projeto

**Dadas a nota de ingresso, a idade na matrícula e a condição de bolsista de um estudante, ele tende a evadir ou a concluir o curso?**

- Tipo de problema: **classificação binária** (`Dropout` = evasão, `Graduate` = conclusão).
- Tema 02 da especificação: *Evasão universitária*.

## 2. Dataset

- **Fonte:** *Predict Students' Dropout and Academic Success*, UCI Machine Learning Repository
  (<https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success>).
  Dados de estudantes de uma instituição de ensino superior portuguesa.
  **Citação:** M.V.Martins, D. Tolledo, J. Machado, L. M.T. Baptista, V.Realinho. (2021) "Early prediction of student’s performance in higher education: a case study" Trends and Applications in Information Systems and Technologies, vol.1, in Advances in Intelligent Systems and Computing series. Springer. DOI: 10.1007/978-3-030-72657-7_16
- **Arquivo no repositório:** `data/dataset.csv` (separador `;`, 4424 linhas × 37 colunas).
- **Classes originais:** Graduate (2209), Dropout (1421) e Enrolled (794).
- **Recorte usado:** apenas `Dropout` e `Graduate`, como pede a especificação. As 794 linhas `Enrolled` (alunos ainda matriculados, sem desfecho definido) são descartadas, restando **3630 registros**.

## 3. Instalação e execução

Testado com **Python 3.12** (Linux). Precisa de **Python 3.12 ou superior**, exigência das versões fixadas de `numpy` e `scipy` no `requirements.txt`.

```bash
# 1. clonar o repositório
git clone https://github.com/OsmarCLFilho/Projeto-TES-Final.git
cd Projeto-TES-Final

# 2. criar e ativar o ambiente virtual
python -m venv venv
source venv/bin/activate          # Linux / macOS
venv\Scripts\Activate.ps1         # Windows (PowerShell)

# 3. instalar as dependências
pip install -r requirements.txt

# 4. rodar a aplicação
python app.py
```

Abra <http://127.0.0.1:5000> no navegador. **Rode sempre a partir da pasta raiz do projeto**, porque os caminhos (`data/`, `static/`, `uploads/`) são relativos.

### Retreinar os modelos (opcional)

Os modelos já treinados estão no repositório (`modelo_decision_tree.pkl` e `modelo_logistico.pkl`). Para gerar de novo:

```bash
python treinar-DecisionTree.py
python treinar-LogisticRegression.py
```

Cada script imprime as métricas no terminal, salva a matriz de confusão em `resultados/` e grava o modelo `.pkl` usado pelo Flask.
O script da Regressão Logística abre a matriz de confusão numa janela (`plt.show()` com backend TkAgg), então precisa de ambiente gráfico.

### Gráficos da base original

Os três gráficos da base original (`static/Grafico*Original.png`) já estão no repositório. Para regerar: `python dados.py`.

## 4. Estrutura do projeto

```
Projeto-TES-Final/
├── app.py                       # rotas Flask, validação do upload e do formulário, previsões
├── dados.py                     # leitura, limpeza, estatísticas e gráficos (Pandas + Matplotlib)
├── treinar-DecisionTree.py      # treino e avaliação da Árvore de Decisão
├── treinar-LogisticRegression.py# treino e avaliação da Regressão Logística
├── modelo_decision_tree.pkl     # modelo treinado (Árvore de Decisão)
├── modelo_logistico.pkl         # modelo treinado (Regressão Logística)
├── requirements.txt
├── data/
│   ├── dataset.csv              # base usada nas análises e no treino
│   └── alunos_simulados.csv     # CSV de exemplo para testar o upload (50 alunos)
├── templates/                   # index, form, previsao, previsaoCsv
├── static/                      # style.css e gráficos gerados
├── resultados/                  # matrizes de confusão, árvore e relatórios (.md)
└── uploads/                     # arquivos CSV enviados pelo usuário
```

## 5. Esquema do CSV aceito

O usuário pode enviar CSVs com registros diferentes, desde que respeitem este formato:

| Coluna | Significado | Tipo | Valores aceitos |
|---|---|---|---|
| `Admission grade` | Nota de ingresso | número | de 0 a 200 |
| `Age at enrollment` | Idade na matrícula | inteiro | de 14 a 100 |
| `Scholarship holder` | Condição de bolsista | binário | `1` = bolsista, `0` = não bolsista |

- Extensão `.csv`, separador `,` ou `;` (detectado automaticamente), uma linha por aluno.
- Outras colunas são ignoradas, e a coluna `Target` não é necessária no upload (é o que o modelo prevê).
- Exemplo (`data/alunos_simulados.csv`):

```csv
Admission grade,Age at enrollment,Scholarship holder
142.5,19,1
118.2,24,0
```

**Validações e mensagens de erro** (`app.py`): arquivo ausente ou sem nome, extensão diferente de `.csv`, colunas obrigatórias ausentes, arquivo vazio ou ilegível, valores não numéricos, e valores fora dos limites acima (inclusive idade não inteira e bolsista diferente de 0 ou 1). Em todos os casos a página do formulário reaparece com uma mensagem em português.

## 6. Tratamento e análise dos dados

A limpeza está em `dados.py`, na função `dataClear`:

| Transformação | Justificativa |
|---|---|
| Remover linhas `Enrolled` | Sem desfecho definido: o problema é evasão × conclusão |
| Manter só as colunas usadas (3 de X + `Target`) | O restante não está disponível no formulário de previsão |
| Remover linhas com valores ausentes (`dropna`) | Modelos escolhidos não aceitam `NaN` |
| **Não** remover duplicatas | A base não tem ID de aluno: linhas iguais nas 4 colunas podem ser alunos diferentes (removê-las apagaria cerca de 23% da base) |

- O CSV original nunca é alterado: toda a limpeza acontece em memória.
- Resultado: 4424 → **3630 linhas**, 37 → 4 colunas. Na base original não há valores ausentes nem duplicatas completas.
- A página de resultados do upload mostra, para cada base: quantidade de registros antes e depois, tipos das colunas, estatísticas descritivas, as transformações aplicadas, uma amostra das 5 primeiras linhas e os achados.

### Achados (base original)

1. **Bolsistas evadem muito menos:** 13,8% de evasão entre bolsistas contra 48,4% entre não bolsistas.
2. **Quem evade entra mais velho:** idade média na matrícula de 26,1 anos (evasão) contra 21,8 (conclusão).
3. **A nota de ingresso quase não separa as classes:** média de 125,0 (evasão) contra 128,8 (conclusão). Por isso a nota sozinha prevê pouco.

### Gráficos

Gerados por `gerarGraficos()` (base original) e `gerarGraficosCsv()` (base enviada) e salvos em `static/`.

| Tipo | Gráfico | Como ler |
|---|---|---|
| Distribuição | Histograma da nota de ingresso | Distribuição concentrada e levemente assimétrica à direita. As notas vão de 95 a 190, com média de 127,3 e mediana de 126,5. Cerca de 75% dos alunos estão entre 110 e 140. Notas acima de 160 são raras (≈2%), o que forma a cauda à direita. Os picos isolados (100, 120, 140, 150) sugerem que muitas notas são arredondadas. |
| Comparação | Taxa de evasão por bolsista | A evasão é de 48,4% entre não bolsistas e 13,8% entre bolsistas, uma diferença de mais de 3 vezes. Os grupos são desiguais: só 26,7% dos alunos (969 de 3630) são bolsistas. A diferença não prova causa, pois a bolsa pode ser concedida a alunos com perfil diferente.|
| Relação | Idade × nota de ingresso, por desfecho | A maioria dos alunos entra entre 17 e 22 anos (68%), e os pontos se acumulam à esquerda. Acima de 25 anos aparecem proporcionalmente mais evasões: 44,4% dos evadidos entram com 25 anos ou mais, contra 15,6% dos concluintes. Na vertical (nota), as duas cores se misturam em todas as faixas, então a nota não separa os desfechos. Isso explica por que os modelos acertam só ≈69%. Há muita sobreposição de pontos, e o gráfico não mostra a densidade.|



## 7. Variáveis X e y

**X (entradas):** informações disponíveis no momento da matrícula.

| Variável | Por que pode ajudar |
|---|---|
| `Admission grade` | Preparação prévia do aluno; nota mais alta pode indicar mais chance de concluir |
| `Age at enrollment` | Alunos que entram mais velhos costumam conciliar estudo e trabalho |
| `Scholarship holder` | A bolsa reduz a pressão financeira |

**y (alvo):** `Target`, com `Dropout` (evasão) ou `Graduate` (conclusão). O alvo não entra em X.

## 8. Modelos testados e comparação

Os dois modelos usam **exatamente a mesma divisão e o mesmo pré-processamento**:

- `train_test_split` com `test_size=0.2`, `random_state=404` e `stratify=y` (as classes mantêm a mesma proporção em treino e teste).
- **Treino:** 2904 registros. **Teste:** 726 registros (284 evasão e 442 conclusão).
- Limpeza feita pela mesma função `dataClear`, importada de `dados.py` pelos dois scripts de treino.

| | Árvore de Decisão | Regressão Logística |
|---|---|---|
| Configuração | `DecisionTreeClassifier(max_depth=5, random_state=404)` | `LogisticRegression(random_state=404)` |
| Acurácia no treino | 71,87% | 69,39% |
| **Acurácia no teste** | **69,28%** | **69,28%** |
| Baseline (sempre prever Conclusão) | 60,88% | 60,88% |
| Precisão (evasão) | 0,64 | 0,68 |
| Sensibilidade/recall (evasão) | 0,50 | 0,41 |
| F1 (evasão) | 0,56 | 0,51 |
| Precisão (conclusão) | 0,72 | 0,70 |
| Sensibilidade/recall (conclusão) | 0,81 | 0,88 |
| F1 (conclusão) | 0,76 | 0,78 |

### Matrizes de confusão (teste, 726 alunos)

| Árvore de Decisão | Previu evasão | Previu conclusão |
|---|---:|---:|
| **Era evasão** | 143 | 141 |
| **Era conclusão** | 82 | 360 |

| Regressão Logística | Previu evasão | Previu conclusão |
|---|---:|---:|
| **Era evasão** | 116 | 168 |
| **Era conclusão** | 55 | 387 |

As imagens estão em `resultados/decisiontree_confusao.png` e `resultados/logistico_confusao.png`. Relatórios completos: `resultados/resultados-decision-tree.md` e `resultados/resultados-logistic.md`.

### Interpretação

- **Os dois modelos empatam em acurácia (69,28%)**, cerca de 8 pontos acima do baseline (60,88%). Ou seja, aprendem algo, mas o ganho é modesto.
- **Overfitting:** a Árvore tem 71,87% no treino contra 69,28% no teste (diferença de 2,6 pontos). A profundidade limitada a 5 segura o problema. A Regressão Logística praticamente não muda (69,39% contra 69,28%).
- **Tipos de erro:** o erro mais custoso é o **falso negativo** (aluno que evade, mas o modelo prevê conclusão), porque o estudante em risco não é identificado. A Árvore deixa passar 141 dos 284 evadidos (**50%**), e a Regressão Logística deixa passar 168 (**59%**). Já os falsos positivos (prever evasão para quem conclui) são 82 na Árvore e 55 na Logística: custam menos, pois levam apenas a um acompanhamento desnecessário.
- Ambos acertam muito mais a classe majoritária (conclusão) do que a evasão.

## 9. Escolha final do modelo

**Modelo escolhido: Árvore de Decisão.**

As acurácias no teste são idênticas (69,28%), então o desempate foi o tipo de erro. O erro mais custoso é o falso negativo (aluno que evade, mas o modelo prevê conclusão). A Árvore tem sensibilidade de 0,50 para evasão, contra 0,41 da Regressão Logística, e deixa passar 141 evadidos, contra 168.

Trade-offs aceitos:
- A Regressão Logística tem precisão maior para evasão (0,68 contra 0,64) e é mais estável entre treino e teste.
- A Árvore tem mais risco de overfitting, mitigado por `max_depth=5` (diferença de 2,6 pontos entre treino e teste), e é mais fácil de explicar (`resultados/arvore_decisao.png`).

## 10. Integração com o Flask

| Rota | Função |
|---|---|
| `GET /` | Página inicial com os gráficos da base original |
| `GET /form` | Formulário: upload de CSV **ou** preenchimento manual (um dos dois) |
| `POST /previsao` | Valida os campos, monta uma linha com as mesmas colunas de X e mostra a previsão dos dois modelos |
| `POST /previsaoCsv` | Valida o CSV, prevê para cada linha, gera estatísticas e gráficos da base enviada e mostra a tabela de previsões |

- Os modelos são carregados com `joblib` na inicialização. **Modelos treinados com `data/dataset.csv`, 3630 registros**
- O CSV enviado atualiza as análises e os gráficos. O modelo permanece fixo.
- Nas estatísticas e gráficos da base enviada, a coluna `Target` é a **previsão do modelo**, não um desfecho real (o usuário não informa o desfecho).

## 11. Limitações

- **Poucas variáveis:** só 3 entradas. O desempenho (≈69%) é modesto e a sensibilidade da evasão não passa de 0,50: metade dos alunos que evadem não é identificada. O resultado é um **estudo didático**, não uma ferramenta de decisão sobre alunos reais.
- **Uma só instituição:** os dados vêm de uma instituição portuguesa, então os resultados podem não valer para outros contextos.
- **Modelo fixo:** não é retreinado quando o usuário envia um CSV. O upload só atualiza análises e previsões.
- **Estatísticas do upload** descrevem o que o modelo prevê, não desfechos reais.
- **Duplicatas:** não removemos duplicatas, pela falta de um identificador de aluno.
- **Arquivos compartilhados:** os gráficos do upload têm nome fixo (`GraficoRelacaoLogistico.png` etc.), então dois usuários ao mesmo tempo sobrescrevem um ao outro. O upload é salvo em `uploads/` com o nome original.
- **Servidor de desenvolvimento:** `app.run(debug=True)`, sem uso em produção.


## 12. Ferramentas utilizadas

- **Dataset:** UCI Machine Learning Repository (ver seção 2).
- **Bibliotecas:** Flask, Pandas, NumPy, Matplotlib, scikit-learn e joblib (versões em `requirements.txt`).