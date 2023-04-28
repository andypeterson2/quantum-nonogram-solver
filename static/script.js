// script.js

// Define some constants for the puzzle size and colors
const ROWS = 3;
const COLS = 3;
const BLACK = "filled";
const WHITE = "marked";
const EMPTY = "";

// Get the HTML elements by their id
const grid = document.getElementById("grid");
const rowClues = document.getElementById("row-clues");
const colClues = document.getElementById("col-clues");
const checkButton = document.getElementById("check");
const resetButton = document.getElementById("reset");
const message = document.getElementById("message");

// Generate a random puzzle and its solution
const puzzle = generatePuzzle(ROWS, COLS);
const solution = solvePuzzle(puzzle);

// Draw the grid and the clues on the page
drawGrid(grid, puzzle);
drawClues(rowClues, puzzle.rowClues);
drawClues(colClues, puzzle.colClues);

// Add event listeners to the buttons
checkButton.addEventListener("click", checkSolution);
resetButton.addEventListener("click", resetGrid);

// Define a function to generate a random puzzle
function generatePuzzle(rows, cols) {
  // Create an empty array to store the puzzle grid
  let grid = [];

  // Loop through the rows and columns and fill each cell randomly with black or white
  for (let i = 0; i < rows; i++) {
    let row = [];
    for (let j = 0; j < cols; j++) {
      let cell = Math.random() < 0.5 ? BLACK : WHITE;
      row.push(cell);
    }
    grid.push(row);
  }

  // Create empty arrays to store the row and column clues
  let rowClues = [];
  let colClues = [];

  // Loop through the rows and columns and calculate the clues for each one
  for (let i = 0; i < rows; i++) {
    rowClues.push(getClues(grid[i]));
  }
  for (let j = 0; j < cols; j++) {
    let col = grid.map(row => row[j]);
    colClues.push(getClues(col));
  }

  // Return an object with the grid and the clues as properties
  return {grid, rowClues, colClues};
}

// Define a function to get the clues for a given array of cells
function getClues(cells) {
  // Create an empty array to store the clues
  let clues = [];

  // Initialize a counter to keep track of the length of each run of black cells
  let count = 0;

  // Loop through the cells and update the count and the clues accordingly
  for (let cell of cells) {
    if (cell === BLACK) {
      // If the cell is black, increment the count by one
      count++;
    } else if (count > 0) {
      // If the cell is not black and the count is positive, push the count to the clues and reset it to zero
      clues.push(count);
      count = 0;
    }
  }

  // If the count is still positive after looping, push it to the clues as well
  if (count > 0) {
    clues.push(count);
  }

  // Return the clues array or [0] if it is empty
  return clues.length > 0 ? clues : [0];
}
function drawGrid(gridElement, puzzle) {
  // Create a table element to represent the grid
  let table = document.createElement("table");

  // Loop through the rows and columns of the puzzle grid
  for (let i = 0; i < puzzle.grid.length; i++) {
    // Create a table row element for each row
    let tr = document.createElement("tr");

    for (let j = 0; j < puzzle.grid[i].length; j++) {
      // Create a table cell element for each cell
      let td = document.createElement("td");

      // Set the class name of the cell according to its value
      td.className = puzzle.grid[i][j];

      // Append the cell to the row
      tr.appendChild(td);
    }

    // Append the row to the table
    table.appendChild(tr);
  }

  // Append the table to the grid element
  gridElement.appendChild(table);
}
function checkSolution() {
  // Get the user's grid from the HTML table
  let userGrid = [];
  let rows = grid.getElementsByTagName("tr");
  for (let i = 0; i < rows.length; i++) {
    let row = [];
    let cells = rows[i].getElementsByTagName("td");
    for (let j = 0; j < cells.length; j++) {
      let cell = cells[j].className;
      row.push(cell);
    }
    userGrid.push(row);
  }

  // Compare the user's grid with the solution grid
  let correct = true;
  for (let i = 0; i < userGrid.length; i++) {
    for (let j = 0; j < userGrid[i].length; j++) {
      if (userGrid[i][j] !== solution[i][j]) {
        correct = false;
        break;
      }
    }
    if (!correct) break;
  }

  // Show a message according to the result
  if (correct) {
    message.textContent = "Congratulations! You solved the puzzle.";
  } else {
    message.textContent = "Sorry, that's not the correct solution. Keep trying!";
  }
}
