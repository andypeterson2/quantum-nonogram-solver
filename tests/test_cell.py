# import unittest
# from src.models.nonogram import Cell, Observer

# class TestObserver(Observer):
#     def __init__(self):
#         self.updated = False

#     def update(self, state):
#         self.updated = True

# class TestCell(unittest.TestCase):
#     def setUp(self):
#         self.cell = Cell()
#         self.observer = TestObserver()
#         self.cell.add_observer(self.observer)

#     def test_cell_default_state(self):
#         self.assertEqual(self.cell.state, False)

#     def test_cell_state_change(self):
#         self.cell.set_state(True)
#         self.assertEqual(self.cell.state, True)

#     def test_observer_notified(self):
#         self.cell.set_state(True)
#         self.assertEqual(self.observer.updated, True)
import unittest
from unittest.mock import Mock
from src.models.cell import Cell

class TestCell(unittest.TestCase):

    def setUp(self):
        # Mocking Observer object
        self.mock_observer = Mock()

        # Creating Cell object with id as 1, state as False, and one observer
        self.cell = Cell(1, False, [self.mock_observer])

    def test_get_id(self):
        # Testing get_id method
        self.assertEqual(self.cell.get_id(), 1)

    def test_get_state(self):
        # Testing get_state method
        self.assertEqual(self.cell.get_state(), False)

    def test_flip(self):
        # Testing flip method
        self.cell.flip()

        # After flipping, the state of cell should be True
        self.assertTrue(self.cell.get_state())

        # Observer's update method should be called once after flipping
        self.mock_observer.update.assert_called_once_with(self.cell)

    def test_update_state(self):
        # Testing update_state method
        self.cell.update_state(True)

        # After updating, the state of cell should be True
        self.assertTrue(self.cell.get_state())

        # Observer's update method should be called once after updating
        self.mock_observer.update.assert_called_once_with(self.cell)

    def test_add_observer(self):
        # Mocking another Observer object
        another_mock_observer = Mock()

        # Adding the new observer
        self.cell.add_observer(another_mock_observer)

        # Now, the cell should have two observers
        self.assertEqual(len(self.cell.observers), 2)

    def test_notify(self):
        # Testing notify method
        self.cell.notify()

        # Observer's update method should be called once after notification
        self.mock_observer.update.assert_called_once_with(self.cell)