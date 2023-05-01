import numpy as np # import arrange, reshape
class Nonogram:
    """Class representing a nonogram puzzle."""
    def __init__(self, rows, columns, row_constraints=None, column_constraints=None, solution=None):
        """Initialize a new nonogram puzzle.
        
        Args:
            rows (int): The number of rows in the puzzle.
            columns (int): The number of columns in the puzzle.
            row_constraints (List[List[int]], optional): The row constraints of the puzzle. Defaults to None.
            column_constraints (List[List[int]], optional): The column constraints of the puzzle. Defaults to None.
            solution (np.ndarray, optional): The given solution to the puzzle. Defaults to None.
        """
        self.rows = rows
        self.columns = columns
        self.row_constraints = row_constraints
        self.column_constraints = column_constraints
        self.given_solution = solution
        self.reached_solution = None
        self.grid_positions = np.arange(self.rows*self.columns).reshape((self.rows, self.columns))

    def __str__(self):
        board = ['╔' + '═'*self.columns + '╗']
        for row in range(self.rows):
            print_row = '║'
            for column in range(self.columns):
                    print_row += '░' if reached_solution[row,column] == 0 else '▓'
            print_row += '║ ' 
            board.append(print_row)
        board.append('╚' + '═'*self.columns + '╝')
        return "\n".join(board)
    
    def update(self, board):
        self.reached_solution = board
        
    # TODO
    def validate(self) -> bool:
        return True
