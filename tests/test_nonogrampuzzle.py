import unittest
from src.models.nonogram import NonogramPuzzle

class TestNonogramPuzzle(unittest.TestCase):
    def setUp(self):
        self.puzzle = NonogramPuzzle(rows=5, columns=5)

    def test_puzzle_size(self):
        self.assertEqual(self.puzzle.rows, 5)
        self.assertEqual(self.puzzle.columns, 5)

    def test_puzzle_cells(self):
        self.assertEqual(len(self.puzzle.cells), 25)

    def test_puzzle_clueboxes(self):
        self.assertEqual(len(self.puzzle.row_clues), 5)
        self.assertEqual(len(self.puzzle.column_clues), 5)

    def test_reset_puzzle(self):
        for cell in self.puzzle.cells:
            cell.set_state(True)
        self.puzzle.reset()
        self.assertTrue(all(cell.state == False for cell in self.puzzle.cells))

    def test_validate_solution_correct(self):
        # Manually set a correct solution
        # Here, we assume that the clues for the puzzle are [[1], [1], [1], [1], [1]] for both rows and columns
        for i in range(5):
            self.puzzle.cells[i * 5].set_state(True)
        self.assertTrue(self.puzzle.validate_solution())

    def test_validate_solution_incorrect(self):
        # Manually set an incorrect solution
        for cell in self.puzzle.cells:
            cell.set_state(True)
        self.assertFalse(self.puzzle.validate_solution())
    def test_validate_solution_correct(self):
        # Manually set a correct solution
        # Here, we assume that the clues for the puzzle are [[1], [1], [1], [1], [1]] for both rows and columns
        # Set a different valid configuration for cells
        for i in range(5):
            self.puzzle.cells[i * 5 + i].set_state(True)

        self.assertTrue(self.puzzle.validate_solution())
