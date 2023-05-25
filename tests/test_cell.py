import unittest
from src.models.nonogram import Cell, Observer

class TestObserver(Observer):
    def __init__(self):
        self.updated = False

    def update(self, state):
        self.updated = True

class TestCell(unittest.TestCase):
    def setUp(self):
        self.cell = Cell()
        self.observer = TestObserver()
        self.cell.add_observer(self.observer)

    def test_cell_default_state(self):
        self.assertEqual(self.cell.state, False)

    def test_cell_state_change(self):
        self.cell.set_state(True)
        self.assertEqual(self.cell.state, True)

    def test_observer_notified(self):
        self.cell.set_state(True)
        self.assertEqual(self.observer.updated, True)
