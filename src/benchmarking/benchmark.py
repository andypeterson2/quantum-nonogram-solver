from abc import ABC, abstractmethod
from src.benchmarking.database import BenchmarkMetrics
import time

class Benchmark(ABC):
    @abstractmethod
    def run(self):
        pass

class TimeBenchmark(Benchmark):
    def __init__(self, solver):
        self.solver = solver

    def run(self, useGPU):
        start_time = time.time()
        steps, _, gates = self.solver.solve(useGPU)
        end_time = time.time()
        time_taken = end_time - start_time
        return BenchmarkMetrics(
            puzzle_size=self.solver.puzzle.rows,
            algorithm=self.solver.algorithm.name,
            steps=steps,
            time=time_taken,
            gates=gates
        )