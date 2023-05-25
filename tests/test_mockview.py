import unittest
from src.models.nonogram import Cell
from src.views.view import MockView

class TestMockView(unittest.TestCase):

    def setUp(self):
        self.mock_view = MockView()
        self.cell = Cell()
        self.cell.add_observer(self.mock_view)

    def test_observer_update(self):
        # Initial state should be False
        self.assertEqual(self.mock_view.cell_state, False)
        # Update cell state
        self.cell.set_state(True)
        # Observer should have updated state
        self.assertEqual(self.mock_view.cell_state, True)
