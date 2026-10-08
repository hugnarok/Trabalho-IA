import unittest

from src.problem import WeightedGrid
from src.heuristics import manhattan
from src.problem import WeightedGrid
from src.search import astar, bfs, dfs, greedy, uniform_cost

def _mapa(*linhas: str) -> WeightedGrid:
    return WeightedGrid([list(linha) for linha in linhas])
class WeightedGridTests(unittest.TestCase):
    def setUp(self):
        self.problem = WeightedGrid.from_file("data/mapa_teste.txt")

    def test_dimensions(self):
        self.assertEqual((self.problem.height, self.problem.width), (8, 16))

    def test_start_and_goal(self):
        self.assertEqual(self.problem.start, (0, 0))
        self.assertEqual(self.problem.goal, (0, 15))

    def test_terrain_costs(self):
        self.assertEqual(self.problem.step_cost((0, 3)), 6)    
        self.assertEqual(self.problem.step_cost((6, 9)), 3)  
        self.assertEqual(self.problem.step_cost((0, 1)), 1)  

    def test_successor_order(self):
        successors = list(self.problem.successors((0, 2)))
        self.assertEqual([a for a, _, _ in successors], ["L", "S", "O"])

class MinimumSearchTests(unittest.TestCase):
    def test_inicio_adjacente_ao_objetivo(self):
        problema = _mapa("SG")
        resultado = bfs(problema)
        self.assertTrue(resultado.found)
        self.assertEqual(resultado.steps, 1)
        self.assertEqual(resultado.cost, 1)
        self.assertEqual(resultado.path, [(0, 0), (0, 1)])
    
    def test_mapa_sem_solucao(self):
        problema = _mapa("S#", "#G")
        for buscar in (bfs, dfs, uniform_cost):
            self.assertFalse(buscar(problema).found)
        self.assertFalse(greedy(problema, manhattan).found)
        self.assertFalse(astar(problema, manhattan).found)
    
    def test_mapa_com_ciclos(self):
        problema = _mapa("S.", ".G")
        
        self.assertIn((0, 0), [pos for _, pos, _ in problema.successors((1, 0))])
        resultado = bfs(problema)
        self.assertTrue(resultado.found)
        self.assertEqual(len(resultado.path), len(set(resultado.path)))

    def test_rotas_distintas_com_o_mesmo_numero_de_acoes(self):
        problema = _mapa("S.", ".G")
        rota_leste = [(0, 0), (0, 1), (1, 1)]
        rota_sul = [(0, 0), (1, 0), (1, 1)]
        self.assertEqual(len(rota_leste) - 1, len(rota_sul) - 1)
        resultado = bfs(problema)
        self.assertEqual(resultado.steps, 2)
        self.assertIn(resultado.path, (rota_leste, rota_sul))
    
    def test_rota_curta_cara_e_rota_longa_barata(self):
        problema = _mapa("SMG", "...")
        em_largura = bfs(problema)
        self.assertEqual(em_largura.steps, 2)
        self.assertEqual(em_largura.cost, 7)
        for buscar in (uniform_cost, lambda p: astar(p, manhattan)):
            resultado = buscar(problema)
            self.assertEqual(resultado.steps, 4)
            self.assertEqual(resultado.cost, 4)
            self.assertEqual(
                resultado.path, [(0, 0), (1, 0), (1, 1), (1, 2), (0, 2)]
            )

if __name__ == "__main__":
    unittest.main()
