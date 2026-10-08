import sys
import time 
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.heuristics import manhattan, euclidean
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
            f"{resultado.peak_frontier:6} {resultado.peak_stored:6} {tempo:12.6f}"
        )

if __name__ == "__main__":
    main()
