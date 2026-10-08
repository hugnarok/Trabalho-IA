import argparse
import json
from random import Random

from .eight_queens import initial_board, render
from .heuristics import euclidean, manhattan
from .hill_climbing import hill_climbing, random_restart
from .problem import WeightedGrid
from .search import astar, bfs, dfs, greedy, uniform_cost


def _search_command(args: argparse.Namespace) -> None:
    problem = WeightedGrid.from_file(args.map)
    heuristics = {"manhattan": manhattan, "euclidean": euclidean}
    if args.algorithm == "bfs":
        result = bfs(problem)
    elif args.algorithm == "dfs":
        result = dfs(problem)
    elif args.algorithm == "ucs":
        result = uniform_cost(problem)
    elif args.algorithm == "greedy":
        result = greedy(problem, heuristics[args.heuristic])
    else:
        result = astar(problem, heuristics[args.heuristic])

    print("\n")
    print("--------------------------------")
    print("Resultados:")
    print("--------------------------------")
    print(f"Algoritmo: {result.algorithm}")
    print(f"Encontrou: {'sim' if result.found else 'não'}")
    print(f"Passos: {result.steps} | Custo: {result.cost}")
    print(f"Gerados: {result.generated} | Expandidos: {result.expanded}")
    print(f"Pico da fronteira: {result.peak_frontier} | Pico de memória: {result.peak_stored_states}")
    if result.found:
        coordenadas = " -> ".join(f"({linha},{coluna})" for linha, coluna in result.path)
        print("Coordenadas:", coordenadas)
        print("Ações:", " ".join(result.actions))
        print("\nCaminho:\n")
        print(problem.render_path(result.path))


def _queens_command(args: argparse.Namespace) -> None:
    rng = Random(args.seed)
    if args.algorithm == "hill":
        board = initial_board(rng)
        result = hill_climbing(board)
    else:
        result = random_restart(rng, max_restarts=args.max_restarts)
    print(json.dumps(result.__dict__, ensure_ascii=False, indent=2))
    print("\nEstado final:\n")
    print(render(result.final))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Trabalho 01 - Inteligência Artificial")
    sub = parser.add_subparsers(dest="part", required=True)

    search_p = sub.add_parser("busca")
    search_p.add_argument("--map", required=True)
    search_p.add_argument(
        "--algorithm", choices=["bfs", "dfs", "ucs", "greedy", "astar"], required=True
    )
    search_p.add_argument(
        "--heuristic", choices=["manhattan", "euclidean"], default="manhattan"
    )
    search_p.set_defaults(func=_search_command)

    queens_p = sub.add_parser("rainhas")
    queens_p.add_argument("--algorithm", choices=["hill", "restart"], required=True)
    queens_p.add_argument("--seed", type=int, default=42)
    queens_p.add_argument("--max-restarts", type=int, default=50)
    queens_p.set_defaults(func=_queens_command)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
