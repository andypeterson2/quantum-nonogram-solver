from src.models.cluebox import ClueBox
from src.models.cell import Cell
class NonogramPuzzle:
    def __init__(self, cells, row_clues=None, column_clues=None):
        self.cells = cells 
        self.rows = len(self.cells)
        self.columns = len(self.cells[0])
        self.row_clues = row_clues
        self.column_clues = column_clues

    def generate_grid_representation(self):
        return [["#" if cell.state else "." for cell in row] for row in self.cells]

    def generate_row_clues_representation(self):
        return [" ".join(str(clue) for clue in row_clues) for row_clues in self.row_clues]

    def generate_column_clues_representation(self):
        max_column_clue_length = max(len(clue) for clue in self.column_clues)
        column_clues_repr = []

        # Initialize all clues with empty strings
        for _ in range(max_column_clue_length):
            column_clues_repr.append([" "]*self.columns)

        # Fill in the clues from bottom to top
        for i, column_clue in enumerate(self.column_clues):
            for j, clue in enumerate(reversed(column_clue)):
                column_clues_repr[j][i] = str(clue)

        return ["".join(column_clue) for column_clue in column_clues_repr]


    def align_grid_and_clues(self, grid_repr, row_clues_repr, column_clues_repr):
        max_row_clue_length = max(len(clue_repr) for clue_repr in row_clues_repr)

        aligned_grid = []
        for clue, row in zip(row_clues_repr, grid_repr):
            aligned_grid.append(clue.rjust(max_row_clue_length) + " " + " ".join(row))

        padding = ["#" * (max_row_clue_length + 2*self.columns - 1)] * len(column_clues_repr)

        return "\n".join(padding + column_clues_repr + aligned_grid)



    def __str__(self):
        grid_repr = self.generate_grid_representation()
        row_clues_repr = self.generate_row_clues_representation()
        column_clues_repr = self.generate_column_clues_representation()

        return self.align_grid_and_clues(grid_repr, row_clues_repr, column_clues_repr)


    def reset(self):
        for row in self.cells:
            for cell in row:
                cell.set_state(False)
        
    def propose_solution(self, board: [[bool]]):
        self.proposed_solution = [list(map(Cell, row)) for row in board]

    def validate_solution(self):
        return all(cluebox.clues == cluebox.calculate_clues() for cluebox in self.row_clues + self.column_clues)