from .algorithm import Algorithm
from ..nonogram import Nonogram
import numpy as np
class Classical(Algorithm):
    """Classical algorithm for solving nonograms."""
    
    def setup(self, data):
        """Setup the classical algorithm with the given data.
        
        Args:
            data (Nonogram): The nonogram to setup the algorithm with.
        """
        pass
    
    def solve(self, data: Nonogram):
        """Solve the given nonogram using a classical algorithm.
        
        Args:
            data (Nonogram): The nonogram to solve.
        
        Returns:
            List[np.ndarray]: A list of all valid solutions to the nonogram.
        """
        # Get the number of rows and columns in the nonogram
        rows = data.rows
        columns = data.columns
        
        # Create a list to store all possible solutions
        solutions = []
        
        # Try all possible combinations of filled and empty cells
        for i in range(2**(rows*columns)):
            # Convert the current combination to binary
            binary = bin(i)[2:].zfill(rows*columns)
            
            # Convert the binary representation to a 2D array
            board = np.array([int(b) for b in binary]).reshape((rows, columns))
            
            # Check if the current combination is a valid solution
            if self.is_valid_solution(data, board):
                solutions.append(board)
        
        # Return all valid solutions
        return solutions
    
    def is_valid_solution(self, data: Nonogram, board: np.ndarray):
        """Check if the given solution is valid according to the constraints of the nonogram.
        
        Args:
            data (Nonogram): The nonogram to check against.
            board (np.ndarray): The solution to check.
        
        Returns:
            bool: True if the solution is valid, False otherwise.
        """
        # Check if the row constraints are satisfied
        for i in range(data.rows):
            row = board[i,:]
            row_segments = self.get_segments(row)
            if row_segments != data.row_constraints[i]:
                return False
    
        # Check if the column constraints are satisfied
        for j in range(data.columns):
            column = board[:,j]
            column_segments = self.get_segments(column)
            if column_segments != data.column_constraints[j]:
                return False
    
        # All constraints are satisfied
        return True

    def get_segments(self, line: np.ndarray):
        """Get the segments of filled cells in a line.
        
        Args:
            line (np.ndarray): The line to get segments from.
        
        Returns:
            List[int]: A list of segment lengths.
        """
        # Get the segments of filled cells in a line
        segments = []
        segment_length = 0
        for cell in line:
            if cell == 1:
                segment_length += 1
            else:
                if segment_length > 0:
                    segments.append(segment_length)
                    segment_length = 0
        if segment_length > 0:
            segments.append(segment_length)
        return segments