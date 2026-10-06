from dataclasses import dataclass, field
from random import Random
from typing import List

from .eight_queens import Board, conflicts, moves, apply_move, initial_board


@dataclass
class HillResult:
    success: bool
    initial: Board
    final: Board
    initial_conflicts: int
    final_conflicts: int
    iterations: int
    evaluated_states: int
    restarts: int = 0
    history: List[int] = field(default_factory=list)

def hill_climbing(initial: Board) -> HillResult:
    current = initial.copy()
    h_cur = conflicts(current)
    iterations = 0
    evaluated = 1  # estado inicial
    history = [h_cur]

    while True:
        best_board = None
        best_h = h_cur

        for mv in moves(current):
            cand = apply_move(current, mv)
            h = conflicts(cand)
            evaluated += 1
            if h < best_h:          # melhora estrita; primeiro melhor
                best_h = h
                best_board = cand

        if best_board is None:      # não há vizinho melhor
            return HillResult(
                success=(h_cur == 0),
                initial=initial,
                final=current,
                initial_conflicts=conflicts(initial),
                final_conflicts=h_cur,
                iterations=iterations,
                evaluated_states=evaluated,
                history=history,
            )

        current = best_board
        h_cur = best_h
        iterations += 1
        history.append(h_cur)

def random_restart(rng: Random, max_restarts: int = 50) -> HillResult:
    total_iter = 0
    total_eval = 0
    restarts = 0
    first_initial = None
    last = None

    # no máximo 51 tentativas: 1 inicial + 50 reinícios
    for attempt in range(max_restarts + 1):
        board = initial_board(rng)
        if first_initial is None:
            first_initial = board.copy()
        else:
            restarts += 1

        result = hill_climbing(board)
        total_iter += result.iterations
        total_eval += result.evaluated_states
        last = result

        if result.success:
            last.restarts = restarts
            last.iterations = total_iter
            last.evaluated_states = total_eval
            last.initial = first_initial
            return last

    last.restarts = restarts
    last.iterations = total_iter
    last.evaluated_states = total_eval
    last.initial = first_initial
    return last