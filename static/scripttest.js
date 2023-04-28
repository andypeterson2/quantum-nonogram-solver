const GRID_SIZE = 10;

const grid = document.querySelector('#grid');

for (let i = 0; i < GRID_SIZE; i++) {
  const row = document.createElement('div');
  row.classList.add('row');
  
  for (let j = 0; j < GRID_SIZE; j++) {
    const cell = document.createElement('div');
    cell.classList.add('cell');
    
    cell.addEventListener('click', () => {
      cell.classList.toggle('on');
    });
    
    row.appendChild(cell);
  }
  
  grid.appendChild(row);
}

const nonogram = new monkeyArms.NonogramSolver('#nonogram', {
  width: GRID_SIZE,
  height: GRID_SIZE,
});

document.querySelector('#solve-button').addEventListener('click', () => {
  const puzzleConditions = [];
  
  for (let i = 0; i < GRID_SIZE; i++) {
    const row = grid.children[i];
    
    for (let j = 0; j < GRID_SIZE; j++) {
      const cell = row.children[j];
      
      if (cell.classList.contains('on')) {
        puzzleConditions.push([i, j]);
      }
    }
  }
  
  nonogram.setPuzzleConditions(puzzleConditions);
  nonogram.solve();
});