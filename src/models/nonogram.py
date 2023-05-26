from src.models.observer import Observer
from .cluebox import ClueBox
from .cell import Cell
from random import choice
class NonogramPuzzle:
    def __init__(self, *, cells=None, rows=None, columns=None, row_clues=None, column_clues=None, algorithm_type='classical'):
        if cells is not None:
            self.cells = cells
            self.row_clues, self.column_clues = self.generate_clues_from_cells(cells)
        elif rows is not None and columns is not None:
            self.rows = rows
            self.columns = columns
            self.cells = self.generate_random_cells(rows, columns)
            self.row_clues, self.column_clues = self.generate_clues_from_cells(self.cells)
        elif row_clues is not None and column_clues is not None:
            self.row_clues = row_clues
            self.column_clues = column_clues
            self.rows = len(row_clues)
            self.columns = len(column_clues)
            self.cells = self.generate_cells_from_clues(row_clues, column_clues)
        else:
            raise ValueError("Invalid arguments for NonogramPuzzle creation")
        self.proposed_solution = None
        self.algorithm = AlgorithmFactory.create_algorithm(algorithm_type)
        self.size = (self.rows, self.columns)
    # def __init__(self, rows, columns, row_clues, column_clues, cells=None):
    #     self.rows = rows
    #     self.columns = columns
    #     self.size = (rows, columns)
    #     if not cells:
    #         self.cells = [Cell() for _ in range(rows * columns)]
    #         self.row_clues = row_clues
    #         self.column_clues = column_clues
    #     else:
    #         self.cells = cells
    #         self.row_clues = [ClueBox(self.cells[i * columns:(i + 1) * columns], clues=[1]) for i in range(rows)]
    #         self.column_clues = [ClueBox([self.cells[i] for i in range(j, rows * columns, columns)], clues=[1]) for j in range(columns)]

    def reset(self):
        for cell in self.cells:
            cell.set_state(False)

    def solve(self):
        self.algorithm.solve()
        
    def propose_solution(self, board: np.ndarray):
        self.proposed_solution = board

    def validate_solution(self):
        return self.proposed_solution == self.cells # Compare based on your implementation

    def validate_solution(self):
        return all(cluebox.clues == cluebox.calculate_clues() for cluebox in self.row_clues + self.column_clues)

    def generate_random_cells(self)