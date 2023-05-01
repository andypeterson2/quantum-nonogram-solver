import pytest
from .algorithm import Algorithm
from .nonogram import Nonogram

@pytest.fixture
def algorithm(request):
    # Create an instance of the given Algorithm subclass
    AlgorithmSubclass = request.param
    return AlgorithmSubclass()

@pytest.mark.parametrize('algorithm', [Classical, Quantum], indirect=True)
def test_algorithm(algorithm):
    # Create a known nonogram puzzle
    rows = 5
    columns = 5
    row_constraints = [[3], [1,1], [5], [1,1], [3]]
    column_constraints = [[3], [1,1], [5], [1,1], [3]]
    nonogram = Nonogram(rows, columns, row_constraints, column_constraints)
    
    # Use the algorithm to solve the nonogram puzzle and measure the runtime
    runtime, solutions = measure_runtime(lambda: algorithm.solve(nonogram))
    
    # Check if the solutions are correct
    expected_solutions = [
        np.array([
            [1, 1, 1, 0, 0],
            [0, 1, 0, 1, 0],
            [1, 1, 1, 1, 1],
            [0, 1, 0, 1, 0],
            [1, 1, 1, 0, 0]
        ])
    ]
    assert solutions == expected_solutions
    
    # Print the runtime of the algorithm
    print(f"Runtime: {runtime:.6f} seconds")