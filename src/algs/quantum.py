from .algorithm import Algorithm
from src.models.nonogram import NonogramPuzzle
from qiskit import IBMQ, Aer, assemble, transpile, QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit.quantum_info.operators import Operator
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import PhaseOracle
from qiskit.algorithms import Grover, AmplificationProblem
from src.benchmarking.database import MemoizationDB
import math
from functools import lru_cache
import sqlite3
import json
from typing import List, Optional
import time

class Quantum(Algorithm):
    name = 'Quantum'
    class BitStringGenerator:
        def __init__(self, memo_db: MemoizationDB):
            self.memo_db = memo_db

        def generate_strings_rec(self, d, l, idx, current, remaining):
            if idx == len(d):
                if remaining >= 0:
                    yield current + [0] * remaining
                return
            for zeros in range(1 if idx > 0 else 0, remaining - d[idx] + 1):
                yield from self.generate_strings_rec(d, l, idx + 1, current + [0] * zeros + [1] * d[idx], remaining - zeros - d[idx])

        def generate_valid_bitstrings(self, l: int, d: List[int]) -> List[str]:
            result = self.memo_db.get_result(l, d)
            if result is None:
                result = [''.join(map(str, b)) for b in self.generate_strings_rec(d, l, 0, [], l)]
                self.memo_db.store_result(l, d, result)
            return result

    def __init__(self, nonogram: NonogramPuzzle, memoizeDB):
        self.nonogram = nonogram
        self.generator = self.BitStringGenerator(memoizeDB)
        # TODO: Fix assumption that num_solutions = 1
        self.num_solutions = 1
        self.iterations = math.ceil(math.pi/4 * math.sqrt(2**(nonogram.rows*nonogram.columns)/self.num_solutions))
        expression = self.to_boolean_expression()
        print("Please wait, this may take a while")
        oracle = PhaseOracle(expression) # TODO: Fix this bottleneck
        problem = AmplificationProblem(oracle=oracle)
        algorithm = Grover(iterations=self.iterations)
        self.circuit = algorithm.construct_circuit(problem)
        self.circuit.measure_all()
        self.gate_count = self.circuit.count_ops()

    def solve(self, useGPU):
        backend = Aer.get_backend('aer_simulator')
        if useGPU:
            backend.set_options(device='GPU')
        job = execute(self.circuit, backend, shots=1024)
        result = job.result()
        sorted_counts = dict(sorted(result.get_counts(self.circuit).items(), key= lambda item: item[1], reverse = True))
        top = dict(list(sorted_counts.items())[:1])
        top_three = dict(list(sorted_counts.items())[:3])
        
        # TODO: Monkeypatch, to be fixed 
        for res in top:
            return self.iterations, res, self.circuit.size()

    def to_boolean_expression(self):
        boolean_statement = ""

        # iterate over row constraints
        for row_idx, row in enumerate(self.nonogram.cells):
            clues = self.nonogram.row_clues[row_idx].clues
            if clues == [0] or clues == []:
                clause = "".join(f'~v{cell.id}&' for cell in row)
                boolean_statement += "(" + clause[:-1] + ")&"
            else:
                bit_strings = self.generator.generate_valid_bitstrings(len(row), clues)
                clauses = []
                for bitstring in bit_strings:
                    clause = ""
                    for column_idx, cell in enumerate(row):
                        if bitstring[column_idx] == '1':
                            clause += f'v{cell.id}&'
                        else:
                            clause += f'~v{cell.id}&'
                    clauses.append("(" + clause[:-1] + ")")
                boolean_statement += "(" + "|".join(clauses) + ")&"

        # iterate over column constraints
        for column_idx in range(self.nonogram.columns):
            clues = self.nonogram.column_clues[column_idx].clues
            if clues == [0]:
                clause = "".join(f'~v{row[column_idx].id}&' for row in self.nonogram.cells)
                boolean_statement += "(" + clause[:-1] + ")&"
            else:
                bit_strings = self.generator.generate_valid_bitstrings(len(self.nonogram.cells), clues)
                clauses = []
                for bitstring in bit_strings:
                    clause = ""
                    for row_idx, row in enumerate(self.nonogram.cells):
                        cell = row[column_idx]
                        if bitstring[row_idx] == '1':
                            clause += f'v{cell.id}&'
                        else:
                            clause += f'~v{cell.id}&'
                    clauses.append("(" + clause[:-1] + ")")
                boolean_statement += "(" + "|".join(clauses) + ")&"

        # remove trailing "&" before returning
        return boolean_statement[:-1]
