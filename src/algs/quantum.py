from .algorithm import Algorithm
from src.models.nonogram import NonogramPuzzle
from qiskit import IBMQ, Aer, assemble, transpile, QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit.quantum_info.operators import Operator
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import PhaseOracle
from qiskit.algorithms import Grover, AmplificationProblem
import math
from functools import lru_cache

class Quantum(Algorithm):
    class Helper:
        @lru_cache(maxsize=None)
        def generate_nonogram_descriptions(l):
            def partition(n):
                if n == 0:
                    return [[]]
                partitions = []
                for p in partition(n-1):
                    partitions.append(p + [1])
                    if p and (len(p) < 2 or p[1] > p[0]):
                        partitions.append([p[0] + 1] + p[1:])
                return partitions
            
            descriptions = partition(l)
            for i in range(1, l):
                descriptions += [d + [0] * (l - sum(d)) for d in partition(i)]
            return sorted(descriptions, key=lambda d: (-len(d), d))

        def generate_bitstrings(l):
            return list(range(2**l))

        def match_description(bitstring, description):
            i = 0
            for d in description:
                group_length = 0
                while i < len(bitstring) and bitstring[i] == '1':
                    group_length += 1
                    i += 1
                if group_length != d:
                    return False
                while i < len(bitstring) and bitstring[i] == '0':
                    i += 1
            return i == len(bitstring)

        def generate_valid_bitstrings(l, d):
            bitstrings = generate_bitstrings(l)
            valid_bitstrings = [b for b in bitstrings if match_description(f'{b:0{l}b}', d)]
            return valid_bitstrings
    def __init__(self, nonogram: NonogramPuzzle):
        self.nonogram = nonogram
        # TODO: Fix assumption that num_solutions = 1
        self.num_solutions = 1
        self.iterations = math.ceil(math.pi/4 * math.sqrt(2**(nonogram.rows*nonogram.columns)/self.num_solutions))
        expression = self.to_boolean_expression()
        oracle = PhaseOracle(expression)
        problem = AmplificationProblem(oracle=oracle)
        algorithm = Grover(iterations=self.iterations)
        self.circuit = algorithm.construct_circuit(problem)
        self.circuit.measure_all()

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
            return res
    
    def to_boolean_expression(self):
        boolean_statement = ""

        # iterate over row constraints
        for row_idx, row in enumerate(self.nonogram.cells):
            clues = self.nonogram.row_clues[row_idx]
            if clues == [0]:
                clause = "".join(f'~v{cell.id}&' for cell in row)
                boolean_statement += "(" + clause[:-1] + ")&"
            else:
                bit_strings = Helper.generate_valid_bitstrings(self.nonogram.columns, clues)
                clauses = []
                for bitstring in bit_strings:
                    clause = ""
                    for column_idx, cell in enumerate(row):
                        if bitstring & (1 << column_idx):
                            clause += f'v{cell.id}&'
                        else:
                            clause += f'~v{cell.id}&'
                    clauses.append("(" + clause[:-1] + ")")
                boolean_statement += "(" + "|".join(clauses) + ")&"

        # iterate over column constraints
        for column_idx in range(self.nonogram.columns):
            clues = self.nonogram.column_clues[column_idx]
            if clues == [0]:
                clause = "".join(f'~v{row[column_idx].id}&' for row in self.nonogram.cells)
                boolean_statement += "(" + clause[:-1] + ")&"
            else:
                bit_strings = Helper.generate_valid_bitstrings(self.nonogram.rows, clues)
                clauses = []
                for bitstring in bit_strings:
                    clause = ""
                    for row_idx, row in enumerate(self.nonogram.cells):
                        cell = row[column_idx]
                        if bitstring & (1 << row_idx):
                            clause += f'v{cell.id}&'
                        else:
                            clause += f'~v{cell.id}&'
                    clauses.append("(" + clause[:-1] + ")")
                boolean_statement += "(" + "|".join(clauses) + ")&"

        # remove trailing "&" before returning
        return boolean_statement[:-1]
