import unittest
from unittest.mock import Mock
from src.models.observer import Observer
from src.models.cell import Cell
from src.views.view import MockView

class TestMockView(unittest.TestCase):

    def setUp(self):
        self.mock_view = MockView()
        self.cell = Cell()

    def test_update(self):
        self.cell.add_observer(self.mock_view)
        self.cell.set_state(True)
        self.assertTrue(self.mock_view.cell_state)

    def test_update_on_flip(self):
        self.cell.add_observer(self.mock_view)
        self.cell.flip()
        self.assertTrue(self.mock_view.cell_state)

    def test_update_multiple_times(self):
        self.cell.add_observer(self.mock_view)
        self.cell.flip()
        self.assertTrue(self.mock_view.cell_state)
        self.cell.flip()
        self.assertFalse(self.mock_view.cell_state)

    def test_multiple_observers(self):
        another_mock_view = MockView()
        self.cell.add_observer(self.mock_view)
        self.cell.add_observer(another_mock_view)
        self.cell.flip()
        self.assertTrue(self.mock_view.cell_state)
        self.assertTrue(another_mock_view.cell_state)