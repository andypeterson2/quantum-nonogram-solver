import unittest
from src.models.nonogram import Cell, ClueBox

class TestClueBox(unittest.TestCase):
    def setUp(self):
        self.cells = [Cell() for _ in range(5)]
        self.cluebox = ClueBox(self.cells, clues=[3])

    def test_cluebox_cells(self):
        self.assertEqual(len(self.cluebox.cells), 5)

    def test_cluebox_clues(self):
        self.assertEqual(self.cluebox.clues, [3])

    def test_cluebox_cells_state_change(self):
        self.cells[0].set_state(True)
        self.cells[1].set_state(True)
        self.cells[2].set_state(True)
        self.assertEqual(self.cluebox.calculate_clues(), [3])

    def test_cluebox_cells_state_change_incorrect(self):
        self.cells[0].set_state(True)
        self.cells[1].set_state(True)
        self.cells[2].set_state(False)
        self.assertNotEqual(self.cluebox.calculate_clues(), [3])
