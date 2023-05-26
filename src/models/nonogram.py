from src.models.cluebox import ClueBox
from src.models.cell import Cell
import numpy as np
class NonogramPuzzle:
    def __init__(self, cells, row_clues=None, column_clues=None):
        self.cells = cells 
        self.rows = len(self.cells)
        self.columns = len(self.cells[0])
        self.row_clues = row_clues
        self.column_clues = column_clues


    def reset(self):
        for row in self.cells:
            for cell in row:
                cell.set_state(False)
        
    def propose_solution(self, board: np.ndarray):
        self.proposed_solution = board

    def validate_solution(self):
        return self.proposed_solution == self.cells # Compare based on your implementation

    def validate_solution(self):
        return all(cluebox.clues == cluebox.calculate_clues() for cluebox in self.row_clues + self.column_clues)