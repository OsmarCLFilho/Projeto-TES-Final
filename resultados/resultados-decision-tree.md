# Resultados - Árvore de Decisão

## 1. Configuração do modelo

- **Modelo utilizado:** Árvore de Decisão (Decision Tree).
- **Base de dados:** Previsão de Abandono e Sucesso Acadêmico.
- **Registros utilizados:** 3.630.
- **Variáveis de entrada (X):**
  - Nota de admissão.
  - Idade ao entrar.
  - Possui bolsa de estudos.
- **Variável de saída (y):** Situação acadêmica.
- **Divisão dos dados:** 80% para treinamento e 20% para teste.
- **Estado aleatório:** 42.

## 2. Resultados da avaliação

- **Taxa de acerto (Acurácia):** 64,33%.

### Matriz de confusão

| | Previu abandono | Previu conclusão |
|---|---:|---:|
| Era abandono | 178 | 99 |
| Era conclusão | 160 | 289 |

### Métricas de avaliação

| Métrica | Abandono | Conclusão |
|---|---:|---:|
| Precisão | 0,53 | 0,74 |
| Sensibilidade | 0,64 | 0,64 |
| Medida F1 | 0,58 | 0,69 |

## 3. Observação

O modelo foi treinado e avaliado utilizando a divisão de 80% para treinamento e 20% para teste.

Esses resultados serão utilizados posteriormente para comparar a Árvore de Decisão com o modelo de Floresta Aleatória.