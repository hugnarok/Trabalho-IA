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
    start = problem.start
    frontier = deque([start])
    frontier_set = {start}
    explored = set()
    parent = {start: None}
    action_to = {start: None}
    cost_so_far = {start: 0.0}

    generated = 1
    expanded = 0
    peak_frontier = 1
    peak_stored = 1

    while frontier:
        peak_frontier = max(peak_frontier, len(frontier))
        peak_stored = max(peak_stored, len(frontier_set | explored))

        node = frontier.popleft()
        frontier_set.remove(node)

        if problem.is_goal_test(node):
            path, actions = _rebuild_path(parent, action_to, start, node)
            return SearchResult(
                found=True,
                algorithm="bfs",
                path=path,
                actions=actions,
                cost=cost_so_far[node],
                generated=generated,
                expanded=expanded,
                peak_frontier=peak_frontier,
                peak_stored=peak_stored,
            )
        explored.add(node)
        expanded += 1

        for action, nxt, step in problem.get_successors(node):
            if nxt not in explored and nxt not in frontier_set:
                parent[nxt] = node
                action_to[nxt] = action
                cost_so_far[nxt] = cost_so_far[node] + step
                frontier.append(nxt)
                frontier_set.add(nxt)
                generated += 1

    return _fail("bfs")

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
