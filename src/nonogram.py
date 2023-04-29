import numpy as np # import arrange, reshape
class Nonogram:
    def __init__(self, rows, columns, row_constraints=None, column_constraints=None, solution=None):
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
