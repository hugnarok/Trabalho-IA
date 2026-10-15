import sys
import time 
from pathlib import Path
from random import Random
from statistics import mean, median

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.eight_queens import conflicts, initial_board, moves, apply_move, render
from src.heuristics import manhattan, euclidean
from src.hill_climbing import hill_climbing, random_restart
from src.problem import WeightedGrid
from src.search import astar, bfs, dfs, greedy, uniform_cost

MAP = Path("data/mapa_teste.txt")
REPETICOES = 30

def _medir(busca, problema):
    tempos = []
    resultados = None
    for _ in range(REPETICOES):
        inicio = time.perf_counter()
        resultado = busca(problema)
        tempos.append(time.perf_counter() - inicio)
    return resultado, median(tempos)

def main() -> None:
    problema = WeightedGrid.from_file(MAP)
    print("\nParte 1: buscas não informadas (BFS, DFS e UCS) e informadas (Gulosa e A*).")
    print(f"Mapa público: {MAP}")
    configuracoes = [
        ("BFS", "-", lambda p: bfs(p)),
        ("DFS", "-", lambda p: dfs(p)),
        ("UCS", "-", lambda p: uniform_cost(p)),
        ("Gulosa", "Manhattan", lambda p: greedy(p, manhattan)),
        ("A*", "Manhattan", lambda p: astar(p, manhattan)),
        ("Gulosa", "Euclidiana", lambda p: greedy(p, euclidean)),
        ("A*", "Euclidiana", lambda p: astar(p, euclidean)),
    ]

    print(f"Mapa: {MAP.name} | repeticoes: {REPETICOES}")
    print(
        f"{'Alg':<8} {'Heur':<12} {'Passos':>6} {'Custo':>8} "
        f"{'Ger':>5} {'Exp':>5} {'PicoF':>6} {'PicoM':>6} {'Tempo_s':>12}"
    )
    for nome, heur, buscar in configuracoes:
        resultado, tempo = _medir(buscar, problema)
        print(
            f"{nome:<8} {heur:<12} {resultado.steps:6} {resultado.cost:8.1f} "
            f"{resultado.generated:5} {resultado.expanded:5} "
            f"{resultado.peak_frontier:6} {resultado.peak_stored_states:6} {tempo:12.6f}"
        )

    rainhas()

def rainhas() -> None:
    print("\nParte 2: 8 Rainhas com Hill Climbing e Random Restart (sementes 0 a 99).")
    hill = [hill_climbing(initial_board(Random(s))) for s in range(100)]
    restart = [random_restart(Random(s), max_restarts=50) for s in range(100)]

    print(f"{'Metrica':<28} {'Hill':>10} {'Restart':>10}")
    for nome, valor in [
        ("Execucoes", len),
        ("Solucoes encontradas", lambda r: sum(x.success for x in r)),
        ("Taxa de sucesso (%)", lambda r: 100 * sum(x.success for x in r) / len(r)),
        ("Media de iteracoes", lambda r: mean(x.iterations for x in r)),
        ("Mediana de iteracoes", lambda r: median(x.iterations for x in r)),
        ("Media de estados avaliados", lambda r: mean(x.evaluated_states for x in r)),
        ("Media de reinicios", lambda r: mean(x.restarts for x in r)),
        ("Maximo de reinicios", lambda r: max(x.restarts for x in r)),
    ]:
        print(f"{nome:<28} {valor(hill):>10.2f} {valor(restart):>10.2f}")

    falhas = [s for s in range(100) if not hill[s].success]
    semente = falhas[0]
    falha = hill[semente]
    vizinhos = [conflicts(apply_move(falha.final, m)) for m in moves(falha.final)]
    print(f"\nPrimeira falha do Hill Climbing: semente {semente}")
    print(f"Estado inicial: {falha.initial} | h = {falha.initial_conflicts}")
    print(f"Estado final:   {falha.final} | h = {falha.final_conflicts}")
    print(f"Valores de h no caminho: {falha.history}")
    print(f"Menor h entre os 56 vizinhos do estado final: {min(vizinhos)} "
          f"({vizinhos.count(min(vizinhos))} vizinhos com esse valor)")
    print(render(falha.final))

if __name__ == "__main__":
    main()
