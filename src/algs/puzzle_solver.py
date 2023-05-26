from .algorithm_factory import AlgorithmFactory
from src.models.nonogram import NonogramPuzzle
class PuzzleSolver:
    def __init__(self, puzzle: NonogramPuzzle, algorithm_name: str):
        self.puzzle = puzzle
        self.algorithm = AlgorithmFactory.create_algorithm(algorithm_name, self.puzzle)

    def solve(self, useGPU=False):
        return self.algorithm.solve(useGPU)