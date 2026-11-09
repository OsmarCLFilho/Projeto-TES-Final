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
- 
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

3. O que é o Índice Gini?

O Índice Gini é utilizado pela Árvore de Decisão para medir o quanto os dados estão misturados em um determinado grupo.

Gini igual a 0: significa que todos os registros daquele grupo pertencem à mesma classe.

Gini maior que 0: significa que existem registros de classes diferentes misturados.

Quanto menor o Gini, mais separados estão os dados.

Durante o treinamento, a Árvore de Decisão calcula o Índice Gini para avaliar diferentes divisões dos dados e escolhe aquelas que conseguem separar melhor as classes.

Esse processo acontece automaticamente, sem precisarmos definir manualmente cada divisão.

No nosso modelo, o Índice Gini ajuda a separar os estudantes nas categorias de abandono e conclusão.

## 4. Observação

O modelo foi treinado e avaliado utilizando a divisão de 80% para treinamento e 20% para teste.

Esses resultados serão utilizados posteriormente para comparar a Árvore de Decisão com outro modelo.