# EC IA - Trabalho 01 - 2026/2

Material público do Trabalho 01 da disciplina de Inteligência Artificial.

## Informações principais

- **Valor:** 20,0 pontos.
- **Modalidade:** individual ou em dupla.
- **Linguagem:** Python.
- **Parte 1 - Busca não informada e informada:** entrega em **08/10/2026**.
- **Parte 2 - Busca local e entrega final:** entrega em **15/10/2026**.

Leia primeiro o arquivo **`EC_IA_Trabalho_01_2026.pdf`**. O enunciado prevalece sobre qualquer resumo apresentado neste README.

## Identificação da entrega

Preencha estes dados antes de cada submissão:

- **Aluno(a) 1:** Hugo Henrique Marques
- **Aluno(a) 2:** João Pedro Silva Siqueira
- **Repositório Git:** https://github.com/hugnarok/Trabalho-IA
- **Tag:** entrega-final

## Como executar

Precisa apenas do Python 3.10 ou mais novo. Não há dependências externas.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/run_experiments.py
python3 -m src.main busca --map data/mapa_teste.txt --algorithm astar --heuristic manhattan
python3 -m src.main rainhas --algorithm hill --seed 42
python3 -m src.main rainhas --algorithm restart --seed 42 --max-restarts 50
```

O script `scripts/run_experiments.py` gera as tabelas das duas partes usadas no relatório.

## Resultados preliminares da Parte 1

Mapa `data/mapa_teste.txt`. Cada configuração foi executada 30 vezes. `Tempo_s` é a mediana, sem contar a leitura do arquivo.

| Alg. | Heur. | Passos | Custo | Ger. | Exp. | Pico F. | Pico mem. | Tempo (s) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| BFS | — | 15 | 40 | 66 | 59 | 9 | 66 | 0.000101 |
| DFS | — | 15 | 40 | 21 | 15 | 6 | 21 | 0.000027 |
| UCS | — | 29 | 29 | 77 | 74 | 6 | 77 | 0.000152 |
| Gulosa | Manhattan | 15 | 40 | 21 | 15 | 6 | 21 | 0.000029 |
| A* | Manhattan | 29 | 29 | 60 | 43 | 15 | 58 | 0.000094 |
| Gulosa | Euclidiana | 15 | 40 | 21 | 15 | 6 | 21 | 0.000028 |
| A* | Euclidiana | 29 | 29 | 72 | 60 | 12 | 72 | 0.000134 |

## Resultados da Parte 2

8 Rainhas, sementes de 0 a 99, Random Restart com limite de 50 reinícios.

| Métrica | Hill Climbing | Random Restart |
|---|---:|---:|
| Taxa de sucesso | 12% | 100% |
| Média de iterações | 3,28 | 24,72 |
| Mediana de iterações | 3 | 17,5 |
| Média de estados avaliados | 240,68 | 1826,64 |
| Média de reinícios | — | 6,76 |
| Máximo de reinícios | — | 42 |

Exemplo de falha do Hill Climbing (semente 0): começa em `[6, 6, 0, 4, 7, 6, 4, 7]` com h = 9 e para em `[6, 3, 5, 2, 1, 6, 4, 7]` com h = 2, sem nenhum vizinho melhor.

## Entrega no SIGAA e repositório Git

O desenvolvimento deve ser mantido em um repositório Git acessível ao professor. O repositório deve permanecer **privado até o encerramento da correção**, com acesso concedido ao professor.

### 08/10/2026 - Parte 1

No SIGAA, envie um arquivo `.zip` com a versão executável da Parte 1. Antes da entrega, crie no repositório a tag:

```bash
git tag entrega-parte1
git push origin entrega-parte1
```

O `README.md` da entrega deve informar o endereço do repositório e a tag `entrega-parte1`. Não é necessário entregar o relatório final nesta etapa.

### 15/10/2026 - Entrega final

No SIGAA, envie:

- o relatório final em PDF;
- um arquivo `.zip` com o projeto completo.

Antes da entrega, crie no repositório a tag:

```bash
git tag entrega-final
git push origin entrega-final
```

O `README.md` e o relatório final devem informar o endereço do repositório e a tag `entrega-final`. A versão avaliada será a versão marcada por essa tag. Commits posteriores não substituem a versão entregue.

O histórico de commits poderá ser utilizado como elemento auxiliar na verificação da autoria e da contribuição dos integrantes, sem exigência de quantidade mínima de commits.

## Conteúdo deste pacote

```text
.
├── EC_IA_Trabalho_01_2026.pdf   # enunciado oficial
├── README.md                     # orientações gerais
├── IA_USAGE.md                   # registro do uso de IA
├── instrucoes_relatorio.md       # orientações para o relatório
├── .gitignore
├── requirements.txt
├── data/
│   └── mapa_teste.txt
├── src/
│   ├── __init__.py
│   ├── problem.py
│   ├── models.py
│   ├── heuristics.py
│   ├── search.py
│   ├── eight_queens.py
│   ├── hill_climbing.py
│   └── main.py
├── scripts/
│   └── run_experiments.py
├── tests/
│   └── test_problem.py
└── modelo_relatorio/
    ├── relatorio_sbc.tex
    └── sbc-template.sty
```

O fonte LaTeX do enunciado e os arquivos institucionais utilizados para sua composição não fazem parte do material de trabalho dos alunos.

## Parte 1 - Busca não informada e informada

Devem ser implementados:

- Busca em Largura - BFS;
- Busca em Profundidade - DFS;
- Busca de Custo Uniforme - UCS;
- Busca Gulosa;
- A*;
- heurísticas Manhattan e Euclidiana.

O mapa público está em `data/mapa_teste.txt`. O programa também será avaliado com mapas não disponibilizados previamente.

Exemplo de execução após a implementação:

```bash
python -m src.main busca --map data/mapa_teste.txt --algorithm astar --heuristic manhattan
```

## Parte 2 - Busca local

Devem ser implementados para o problema das 8 Rainhas:

- Hill Climbing;
- Random-Restart Hill Climbing.

Exemplos:

```bash
python -m src.main rainhas --algorithm hill --seed 42
python -m src.main rainhas --algorithm restart --seed 42 --max-restarts 50
```

## Teste inicial do código-base

Antes de implementar os algoritmos, execute:

```bash
python -m unittest discover -s tests -v
```

Os testes fornecidos verificam apenas a infraestrutura inicial. A equipe deve adicionar os casos de teste exigidos no enunciado.

## Experimentos

O arquivo `scripts/run_experiments.py` é um esqueleto para a execução padronizada dos experimentos utilizados no relatório. Ele deve ser completado pela equipe.

## Relatório

Consulte `instrucoes_relatorio.md` e a pasta `modelo_relatorio/`.

O relatório deve usar o modelo SBC fornecido, sem capa separada, respeitando o limite e os requisitos definidos no enunciado.

## Uso de Inteligência Artificial

Todo uso de ferramentas de IA deve obedecer à política descrita no enunciado e ser registrado em `IA_USAGE.md`.

## Observação importante

As funções correspondentes aos algoritmos e às heurísticas estão deliberadamente incompletas. O código fornecido é apenas a infraestrutura inicial do trabalho e não contém o gabarito das implementações.
