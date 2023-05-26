from .algorithm import Algorithm
from .classical import Classical
from .quantum import Quantum

class AlgorithmFactory:
    """Factory class for creating instances of Algorithm subclasses."""

    @staticmethod
    def create_algorithm(type: str, *args, **kwargs) -> Algorithm:
        """Create and return an instance of the specified algorithm type.

        Args:
            type (str): The type of algorithm to create.

        Returns:
            Algorithm: An instance of the specified algorithm type.
        """
        if type == 'classical':
            return Classical(*args, **kwargs)
        elif type == 'quantum':
            return Quantum(*args, **kwargs)
        else:
            raise ValueError(f"Invalid algorithm type: {type}")
