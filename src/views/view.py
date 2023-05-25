from src.models.observer import Observer
from src.models.nonogram import Cell
class MockView(Observer):
    def __init__(self):
        self.cell_state = False

    def update(self, cell: Cell):
        self.cell_state = cell.state
        print(f'Cell state updated to {cell.state}')