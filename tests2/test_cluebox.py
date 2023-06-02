import unittest
from src.models.cell import Cell
from src.models.cluebox import ClueBox

class TestClueBox(unittest.TestCase):

    def setUp(self):
        self.cells = [Cell(False) for _ in range(10)]
        self.clues = [2, 3, 1]
        self.clue_box = ClueBox(self.cells, self.clues)

    def test_calculate_clues_no_active_cells(self):
        clues_calculated = self.clue_box.calculate_clues()
        self.assertEqual(clues_calculated, [0])

    def test_calculate_clues_some_active_cells(self):
        self.cells[0].set_state(True)
        self.cells[1].set_state(True)
        self.cells[3].set_state(True)
        self.cells[4].set_state(True)
        self.cells[5].set_state(True)
        self.cells[7].set_state(True)
        clues_calculated = self.clue_box.calculate_clues()
        self.assertEqual(clues_calculated, [2, 3, 1])

    def test_calculate_clues_all_active_cells(self):
        for cell in self.cells:
            cell.set_state(True)
        clues_calculated = self.clue_box.calculate_clues()
        self.assertEqual(clues_calculated, [10])