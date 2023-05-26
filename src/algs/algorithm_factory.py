from .algorithm import Algorithm
from .classical import Classical
from .quantum import Quantum
from src.models.nonogram import NonogramPuzzle

class AlgorithmFactory:
    """Factory class for creating instances of Algorithm subclasses."""

    @staticmethod
    def create_algorithm(type: str, puzzle: NonogramPuzzle) -> Algorithm:
        """Create and return an instance of the specified algorithm type.

        Args:
            type (str): The type of algorithm to create.
            puzzle (NonogramPuzzle): The nonogram to solve

        Returns:
            Algorithm: An instance of the specified algorithm type.
        """
        if type == 'classical':
            return Classical(puzzle)
        elif type == 'quantum':
            return Quantum(puzzle)
        else:
            raise ValueError(f"Invalid algorithm type: {type}")
