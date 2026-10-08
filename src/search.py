from collections.abc import Callable
from collections import deque
import heapq
from os import path
from tracemalloc import start

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

def _fail(algorithm, generated, expanded, peak_frontier, peak_stored):
    return SearchResult(
        found=False,
        algorithm=algorithm,
        generated=generated,
        expanded=expanded,
        peak_frontier=peak_frontier,
        peak_stored_states=peak_stored,
    )

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
        peak_stored = max(peak_stored, len(frontier_set) + len(explored))

        node = frontier.popleft()
        frontier_set.remove(node)

        if problem.goal_test(node):
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
                peak_stored_states=peak_stored,
            )
        explored.add(node)
        expanded += 1

        for action, nxt, step in problem.successors(node):
            if nxt not in explored and nxt not in frontier_set:
                parent[nxt] = node
                action_to[nxt] = action
                cost_so_far[nxt] = cost_so_far[node] + step
                frontier.append(nxt)
                frontier_set.add(nxt)
                generated += 1

    return _fail("bfs", generated, expanded, peak_frontier, peak_stored)

def dfs(problem: WeightedGrid) -> SearchResult:
    start = problem.start
    frontier = [start]
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
        peak_stored = max(peak_stored, len(frontier_set) + len(explored))

        node = frontier.pop()
        frontier_set.remove(node)

        if problem.goal_test(node):
            path, actions = _rebuild_path(parent, action_to, start, node)
            return SearchResult(
                found=True,
                algorithm="dfs",
                path=path,
                actions=actions,
                cost=cost_so_far[node],
                generated=generated,
                expanded=expanded,
                peak_frontier=peak_frontier,
                peak_stored_states=peak_stored,
            )
        
        explored.add(node)
        expanded += 1

        succs = list(problem.successors(node))
        for action, nxt, step in reversed(succs):
            if nxt not in explored and nxt not in frontier_set:
                parent[nxt] = node
                action_to[nxt] = action
                cost_so_far[nxt] = cost_so_far[node] + step
                frontier.append(nxt)
                frontier_set.add(nxt)
                generated += 1

    return _fail("dfs", generated, expanded, peak_frontier, peak_stored)

def uniform_cost(problem: WeightedGrid) -> SearchResult:
    """Busca de Custo Uniforme. Implemente conforme a especificação do trabalho."""
    start = problem.start
    counter = 0
    frontier = [(0.0, counter, start)]
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
        peak_frontier = max(peak_frontier, len(frontier_set))
        peak_stored = max(peak_stored, len(frontier_set) + len(explored))

        g, _, node = heapq.heappop(frontier)
        # entrada obsoleta: estado já expandido ou custo melhor já registrado
        if node in explored or g > cost_so_far[node]:
            continue
        frontier_set.remove(node)

        if problem.goal_test(node):
            path, actions = _rebuild_path(parent, action_to, start, node)
            return SearchResult(
                found=True,
                algorithm="ucs",
                path=path,
                actions=actions,
                cost=cost_so_far[node],
                generated=generated,
                expanded=expanded,
                peak_frontier=peak_frontier,
                peak_stored_states=peak_stored,
            )

        explored.add(node)
        expanded += 1

        for action, nxt, step in problem.successors(node):
            if nxt in explored:
                continue
            new_cost = cost_so_far[node] + step
            if nxt not in frontier_set or new_cost < cost_so_far[nxt]:
                parent[nxt] = node
                action_to[nxt] = action
                cost_so_far[nxt] = new_cost
                counter += 1
                heapq.heappush(frontier, (new_cost, counter, nxt))
                frontier_set.add(nxt)
                generated += 1

    return _fail("ucs", generated, expanded, peak_frontier, peak_stored)


def greedy(problem: WeightedGrid, heuristic: Heuristic) -> SearchResult:
    start = problem.start
    goal = problem.goal
    counter = 0
    h0 = heuristic(start, goal)
    frontier = [(h0, counter, start)]
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
        peak_stored = max(peak_stored, len(frontier_set) + len(explored))
        
        _, _, node = heapq.heappop(frontier)
        if node not in frontier_set:
            continue
        frontier_set.remove(node)

        if problem.goal_test(node):
            path, actions = _rebuild_path(parent, action_to, start, node)
            return SearchResult(
                found=True,
                algorithm="greedy",
                path=path,
                actions=actions,
                cost=cost_so_far[node],
                generated=generated,
                expanded=expanded,
                peak_frontier=peak_frontier,
                peak_stored_states=peak_stored,
            )
        
        explored.add(node)
        expanded += 1

        for action, nxt, step in problem.successors(node):
            if nxt not in explored and nxt not in frontier_set:
                parent[nxt] = node
                action_to[nxt] = action
                cost_so_far[nxt] = cost_so_far[node] + step
                counter += 1
                heapq.heappush(frontier, (heuristic(nxt, goal), counter, nxt))
                frontier_set.add(nxt)
                generated += 1

    return _fail("greedy", generated, expanded, peak_frontier, peak_stored)

def astar(problem: WeightedGrid, heuristic: Heuristic) -> SearchResult:
    """Busca A*."""
    start = problem.start
    goal = problem.goal
    counter = 0
    h0 = heuristic(start, goal)
    frontier = [(h0, h0, counter, 0.0, start)]  # (f, h, ordem de inserção, g, estado)
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
        peak_frontier = max(peak_frontier, len(frontier_set))
        peak_stored = max(peak_stored, len(frontier_set) + len(explored))

        _, _, _, g, node = heapq.heappop(frontier)
        # entrada obsoleta: estado já expandido ou custo melhor já registrado
        if node in explored or g > cost_so_far[node]:
            continue
        frontier_set.remove(node)

        if problem.goal_test(node):
            path, actions = _rebuild_path(parent, action_to, start, node)
            return SearchResult(
                found=True,
                algorithm="astar",
                path=path,
                actions=actions,
                cost=cost_so_far[node],
                generated=generated,
                expanded=expanded,
                peak_frontier=peak_frontier,
                peak_stored_states=peak_stored,
            )

        explored.add(node)
        expanded += 1

        for action, nxt, step in problem.successors(node):
            if nxt in explored:
                continue
            new_cost = cost_so_far[node] + step
            if nxt not in frontier_set or new_cost < cost_so_far[nxt]:
                parent[nxt] = node
                action_to[nxt] = action
                cost_so_far[nxt] = new_cost
                counter += 1
                h = heuristic(nxt, goal)
                heapq.heappush(frontier, (new_cost + h, h, counter, new_cost, nxt))
                frontier_set.add(nxt)
                generated += 1

    return _fail("astar", generated, expanded, peak_frontier, peak_stored)
