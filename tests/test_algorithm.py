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