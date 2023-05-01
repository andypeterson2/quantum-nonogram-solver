from abc import ABC, abstractmethod

class Algorithm(ABC):
    """Abstract base class for nonogram solving algorithms."""
    
    @abstractmethod
    def solve(self, data):
        """Solve the given nonogram.
        
        Args:
            data (Nonogram): The nonogram to solve.
        
        Returns:
            Any: The solution to the nonogram.
        """
        pass
    
    @abstractmethod
    def setup(self, data):
        """Setup the algorithm with the given data.
        
        Args:
            data (Nonogram): The nonogram to setup the algorithm with.
        """
        pass