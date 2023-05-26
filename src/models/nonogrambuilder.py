from .nonogram import NonogramPuzzle
from .cell import Cell
from random import choice

class NonogramBuilder:
    def __init__(self):
        self.cells = None
        self.rows = None
        self.columns = None
        self.row_clues = None
        self.column_clues = None

    # Specification methods
    def with_cells(self, cells):
        # TODO: add input validation
        self.cells = [[Cell(state=cell_value) for cell_value in row] for row in cells]
        return self

    def with_size(self, rows, columns=None):
        # TODO: add input validation
        self.rows = rows
        # Assumes square size if not specified.
        self.columns = rows if columns is None else columns 
        return self

    def with_clues(self, row_clues, column_clues):
        # TODO: add input validation
        self.row_clues = row_clues
        self.column_clues = column_clues
        self.rows = len(row_clues)
        self.columns = len(column_clues)
        return self
    
    # Board generation methods
    def generate_random(self):
        cells = [[Cell(choice([True, False])) for _ in range(self.columns)] for _ in range(self.rows)]
        self._assign_ids(cells)
        return cells

    def generate_from_boolean_array(self, boolean_array):
        cells = [[Cell(value) for value in row] for row in boolean_array]
        self._assign_ids(cells)
        return cells

    def generate_from_clues(self):
        cells = [[Cell(False) for _ in range(self.columns)] for _ in range(self.rows)]
        self._assign_ids(cells)
        return cells
    
    # Misc methods
    def generate_clues_from_cells(self):
        # Create row clues
        row_clues = []
        for row in self.cells:
            clue = []
            count = 0
            for cell in row:
                if cell.state:
                    count += 1
                elif count > 0:
                    clue.append(count)
                    count = 0
            if count > 0:
                clue.append(count)
            row_clues.append(clue)

        # Create column clues
        column_clues = []
        for column in zip(*self.cells):
            clue = []
            count = 0
            for cell in column:
                if cell.state:
                    count += 1
                elif count > 0:
                    clue.append(count)
                    count = 0
            if count > 0:
                clue.append(count)
            column_clues.append(clue)

        return row_clues, column_clues
    
    def _assign_ids(self, cells):
        id_counter = 1
        for row in cells:
            for cell in row:
                cell.id = id_counter
                id_counter += 1

    # Build method
    def build(self):
        if self.cells is not None:
            # Specified by board configuration; implied size and clues
            puzzle = NonogramPuzzle(cells=self.cells)
            
        elif self.row_clues is not None and self.column_clues is not None:
            # Specified by clues
            self.cells = self.generate_from_clues()
            puzzle = NonogramPuzzle(cells=self.cells, row_clues=self.row_clues, column_clues=self.column_clues)
        
        elif self.rows is not None and self.columns is not None:
            # Specified by size; random config
            self.cells = self.generate_random()
            puzzle = NonogramPuzzle(cells=self.cells)
        else:
            raise ValueError("Invalid setup for Nonogram creation")
            
        if puzzle.cells is not None and (puzzle.row_clues is None or puzzle.column_clues is None):
            puzzle.row_clues, puzzle.column_clues = self.generate_clues_from_cells()
            puzzle.reset()

        return puzzle