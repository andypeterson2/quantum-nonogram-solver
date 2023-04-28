import random

ROWS = 3
COLS = 3
BLACK = "filled"
WHITE = "marked"
EMPTY = ""

def generate_puzzle(rows, cols):
    # Create an empty list to store the puzzle grid
    grid = []

    # Loop through the rows and columns and fill each cell randomly with black or white
    for i in range(rows):
        row = []
        for j in range(cols):
            cell = BLACK if random.random() < 0.5 else WHITE
            row.append(cell)
        grid.append(row)

    # Create empty lists to store the row and column clues
    rowClues = []
    colClues = []

    # Loop through the rows and columns and calculate the clues for each one
    for i in range(rows):
        rowClues.append(getClues(grid[i]))
    for j in range(cols):
            col = [row[j] for row in grid]
            colClues.append(getClues(col))

    # Return a dictionary with the grid and the clues as keys
    return {"grid": grid, "row_clues": rowClues, "col_clues": colClues}

def getClues(cells):
    # Create an empty list to store the clues
    clues = []

    # Initialize a counter to keep track of the length of each run of black cells
    count = 0

    # Loop through the cells and update the count and the clues accordingly
    for cell in cells:
        if cell == BLACK:
        # If the cell is black, increment the count by one
            count += 1
        elif count > 0:
        # If the cell is not black and the count is positive, append the count to the clues and reset it to zero
            clues.append(count)
            count = 0

    # If the count is still positive after looping, append it to the clues as well
    if count > 0:
        clues.append(count)

    # Return the clues list or [0] if it is empty
    return clues if clues else [0]


