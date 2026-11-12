# Resultados - Árvore de Decisão

## 1. Configuração do modelo

- **Modelo utilizado:** Regressão Logística (Logistic Regression).
- **Base de dados:** Previsão de Abandono e Sucesso Acadêmico.
- **Registros utilizados:** 3.630.
- **Variáveis de entrada (X):**
  - Nota de admissão.
  - Idade ao entrar.
  - Possui bolsa de estudos.
- **Variável de saída (y):** Situação acadêmica.
- **Divisão dos dados:** 80% para treinamento e 20% para teste.
- **Estado aleatório:** 404.

## 2. Resultados da avaliação

- **Acurácia no treinamento:** 69,39%.
- **Taxa de acerto no teste (Acurácia):** 69,28%.
- **Baseline:** 60,88%.

### Matriz de confusão

| | Previu abandono | Previu conclusão |
|---|---:|---:|
| Era abandono | 116 | 168 |
| Era conclusão | 55 | 387 |

### Métricas de avaliação

| Métrica | Abandono | Conclusão |
|---|---:|---:|
| Precisão | 0,68 | 0,70 |
| Sensibilidade | 0,41 | 0,88 |
| Medida F1 | 0,51 | 0,78 |

## 4. Observação

O modelo foi treinado utilizando 80% dos dados e avaliado com os 20% restantes.

A acurácia no teste foi de 69,28%, enquanto o baseline apresentou 60,88%. Isso significa que a Regressão Logística teve um resultado melhor do que simplesmente prever a classe mais comum.

A acurácia de treinamento foi de 69,38%, um resultado próximo ao obtido no teste.

Esses resultados serão utilizados posteriormente para comparar a Regressão Logística com outro modelo.
