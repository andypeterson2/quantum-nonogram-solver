# import pytest
# from src.algs import Algorithm, Classical, Quantum
# from src.models.nonogram import Nonogram
# from abc import ABC, abstractmethod
# import time

# class Maybe(ABC):
#     @abstractmethod
#     def __init__(self, value):
#         pass
    
#     @abstractmethod
#     def bind(self, function):
#         pass
    
# class Just(Maybe):
#     def __init__(self, value):
#         self.value = value
        
#     def bind(self, function):
#         return function(self.value)
    
# class Nothing(Maybe):
#     def bind(self, function):
#         return self
        
# def measure_runtime(func):
#     start = time.time()
#     result = Just(func()).bind(lambda x: x)
#     end = time.time()
#     return runtime, result

# @pytest.fixture
# def algorithm(request):
#     # Create an instance of the given Algorithm subclass
#     AlgorithmSubclass = request.param
#     return AlgorithmSubclass()

# @pytest.mark.parametrize('algorithm', [Classical, Quantum], indirect=True)
# def test_algorithm(algorithm):
#     # Create a known nonogram puzzle
#     rows = 2
#     columns = 2
#     row_constraints = [[1], [0]]
#     column_constraints = [[0], [0]]
#     nonogram = Nonogram(rows, columns, row_constraints, column_constraints)
#     print("Beginning solve")
#     # Use the algorithm to solve the nonogram puzzle and measure the runtime
#     runtime, solutions = measure_runtime(lambda: algorithm.solve(nonogram))
    
#     # Check if the solutions are correct
#     expected_solutions = [
#         np.array([
#             [1, 0],
#             [0, 0],
#         ])
#     ]
#     assert solutions == expected_solutions
    
#     # Print the runtime of the algorithm
#     print(f"Runtime: {runtime:.6f} seconds")
import unittest
from src.models.nonogram import NonogramPuzzle
from src.solver.algorithm import Algorithm, ClassicalSolver

class TestAlgorithm(unittest.TestCase):
    def setUp(self):
        self.algorithm = Algorithm()

    def test_abstract_methods(self):
        with self.assertRaises(NotImplementedError):
            self.algorithm.setup(None)

        with self.assertRaises(NotImplementedError):
            self.algorithm.solve(None)


class TestClassicalSolver(unittest.TestCase):
    def setUp(self):
        self.solver = ClassicalSolver()
        # Prepare a simple 2x2 NonogramPuzzle for testing
        cells = [False, True, True, False]
        rows = 2
        columns = 2
        row_clues = [[1], [1]]
        col_clues = [[1], [1]]
        self.nonogram = NonogramPuzzle(cells, rows, columns, row_clues, col_clues)

    def test_setup(self):
        self.solver.setup(self.nonogram)
        # Test if the solver correctly set up the nonogram puzzle
        self.assertEqual(self.solver.data, self.nonogram)

    def test_solve(self):
        # Test if the solver returns the correct solution
        expected_solution = [[False, True], [True, False]]
        self.assertEqual(self.solver.solve(self.nonogram), expected_solution)
