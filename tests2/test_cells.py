import unittest
from unittest.mock import Mock
from src.models.observer import Observer
from src.models.cell import Cell

class TestCell(unittest.TestCase):

    def setUp(self):
        self.mock_observer = Mock(Observer)
        self.cell = Cell()

    def test_add_observer(self):
        self.cell.add_observer(self.mock_observer)
        self.assertIn(self.mock_observer, self.cell.observers)

    def test_add_observer_invalid(self):
        with self.assertRaises(TypeError):
            self.cell.add_observer("Not an observer")

    def test_set_state(self):
        self.cell.add_observer(self.mock_observer)
        self.cell.set_state(True)
        self.assertTrue(self.cell.state)
        self.mock_observer.update.assert_called_once()

    def test_flip_state(self):
        self.cell.add_observer(self.mock_observer)
        self.cell.flip()
        self.assertTrue(self.cell.state)
        self.mock_observer.update.assert_called_once()

    def test_notify_observers(self):
        self.cell.add_observer(self.mock_observer)
        self.cell.notify_observers()
        self.mock_observer.update.assert_called_once()

    def test_str(self):
        self.assertEqual(str(self.cell), str(self.cell.state))
