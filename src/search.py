from collections.abc import Callable
from collections import deque
import heapq
from os import path

from .models import SearchResult
from .problem import WeightedGrid

Heuristic = Callable[[tuple[int, int], tuple[int, int]], float]

def _rebuild_path(parent, action_to, start, goal):
    path = [goal]
    actions = []
    cur = goal
    while cur != start:
        actions.append(action_to[cur])
        cur = parent[cur]
        path.append(cur)
    path.reverse()
    actions.reverse()
    return path, actions

def _fail(algorithm):
    return SearchResult(found=False, algorithm=algorithm)

def bfs(problem: WeightedGrid) -> SearchResult:
    """Busca em Largura. Implemente conforme a especificação do trabalho."""
    raise NotImplementedError("Implemente BFS.")


def dfs(problem: WeightedGrid) -> SearchResult:
    """Busca em Profundidade. Implemente conforme a especificação do trabalho."""
    raise NotImplementedError("Implemente DFS.")


def uniform_cost(problem: WeightedGrid) -> SearchResult:
    """Busca de Custo Uniforme. Implemente conforme a especificação do trabalho."""
    raise NotImplementedError("Implemente UCS.")


def greedy(problem: WeightedGrid, heuristic: Heuristic) -> SearchResult:
    """Busca Gulosa pelo melhor primeiro."""
    raise NotImplementedError("Implemente Busca Gulosa.")


def astar(problem: WeightedGrid, heuristic: Heuristic) -> SearchResult:
    """Busca A*."""
    raise NotImplementedError("Implemente A*.")
