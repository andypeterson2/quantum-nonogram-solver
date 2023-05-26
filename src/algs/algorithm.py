from abc import ABC, abstractmethod

class Algorithm(ABC):
    """Abstract base class for nonogram solving algorithms."""
    
    @abstractmethod
    def solve(self):
        """Solve the given nonogram.
        Returns:
            Any: The solution to the nonogram.
        """
        pass