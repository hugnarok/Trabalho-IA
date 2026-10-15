import unittest
from random import Random

from src.eight_queens import conflicts, initial_board, moves
from src.hill_climbing import hill_climbing, random_restart


class EightQueensTests(unittest.TestCase):
    def test_solucao_sem_conflitos(self):
        self.assertEqual(conflicts([3, 6, 2, 7, 1, 4, 0, 5]), 0)

    def test_todas_na_mesma_linha(self):
        self.assertEqual(conflicts([0] * 8), 28)

    def test_vizinhanca(self):
        vizinhos = list(moves([0] * 8))
        self.assertEqual(len(vizinhos), 56)
        self.assertEqual(vizinhos[:2], [(0, 1), (0, 2)])
        self.assertEqual(vizinhos[-1], (7, 7))


class HillClimbingTests(unittest.TestCase):
    def test_hill_climbing_so_aceita_melhora(self):
        resultado = hill_climbing(initial_board(Random(0)))
        historico = resultado.history
        for antes, depois in zip(historico, historico[1:]):
            self.assertLess(depois, antes)
        self.assertEqual(resultado.iterations, len(historico) - 1)
        self.assertEqual(resultado.evaluated_states, 1 + 56 * (resultado.iterations + 1))

    def test_hill_climbing_para_sem_solucao(self):
        resultado = hill_climbing([6, 6, 0, 4, 7, 6, 4, 7])
        self.assertFalse(resultado.success)
        self.assertEqual(resultado.final_conflicts, 2)

    def test_random_restart_limite_de_reinicios(self):
        resultado = random_restart(Random(0), max_restarts=0)
        self.assertEqual(resultado.restarts, 0)
        for semente in range(100):
            self.assertLessEqual(random_restart(Random(semente), 50).restarts, 50)

    def test_mesma_semente_mesmo_resultado(self):
        a = random_restart(Random(7), 50)
        b = random_restart(Random(7), 50)
        self.assertEqual((a.final, a.restarts), (b.final, b.restarts))


if __name__ == "__main__":
    unittest.main()
