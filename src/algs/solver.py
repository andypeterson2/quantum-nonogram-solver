from .algorithm_factory import AlgorithmFactory
from src.models.nonogram import NonogramPuzzle
class Solver:
    def __init__(self, puzzle: NonogramPuzzle, algorithm_name: str, db_name = ':memory:'):
        self.puzzle = puzzle
        self.algorithm = AlgorithmFactory.create_algorithm(algorithm_name, self.puzzle, db_name)

    def solve(self, useGPU=False):
        return self.algorithm.solve(useGPU)