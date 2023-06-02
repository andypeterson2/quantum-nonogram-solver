import unittest
import numpy as np
from src.models.cell import Cell
from src.models.cluebox import ClueBox
from src.models.nonogram import NonogramPuzzle

class TestNonogramPuzzle(unittest.TestCase):

    def setUp(self):
        self.cells = [[Cell(False) for _ in range(10)] for _ in range(10)]
        self.row_clues = [ClueBox(self.cells[i], [3, 2]) for i in range(10)]
        self.column_clues = [ClueBox([self.cells[j][i] for j in range(10)], [2, 3]) for i in range(10)]
        self.puzzle = NonogramPuzzle(self.cells, self.row_clues, self.column_clues)

    def test_reset(self):
        for row in self.cells:
            for cell in row:
                cell.set_state(True)
        self.puzzle.reset()
        for row in self.cells:
            for cell in row:
                self.assertFalse(cell.state)

    def test_propose_solution(self):
        proposed_solution = np.ones((10, 10), dtype=bool)
        self.puzzle.propose_solution(proposed_solution)
        self.assertTrue((self.puzzle.proposed_solution == proposed_solution).all())

    # TODO: Fix
    # def test_validate_solution(self):
    #     proposed_solution = np.ones((10, 10), dtype=bool)
    #     self.puzzle.propose_solution(proposed_solution)
    #     for row in self.cells:
    #         for cell in row:
    #             cell.set_state(True)
    #     self.assertTrue(self.puzzle.validate_solution())

