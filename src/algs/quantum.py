from .algorithm import Algorithm
from src.models.nonogram import NonogramPuzzle
from qiskit import IBMQ, Aer, assemble, transpile, QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit.quantum_info.operators import Operator
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import PhaseOracle
from qiskit.algorithms import Grover, AmplificationProblem
import math
class Quantum(Algorithm):
    possible_d = {
                # l = 1
                "1/0;" : [0b0],
                "1/1;" : [0b1],

                # l = 2
                "2/0;" : [0b00],
                "2/1;" : [0b01,0b10],
                "2/2;" : [0b11],

                # l = 3
                "3/0;" : [0b000],
                "3/1;" : [0b100, 0b010,0b001],
                "3/2;" : [0b110,0b011],
                "3/3;" : [0b111],
                "3/1;1;" : [0b101],

                # l = 4
                "4/0;" : [0b0000],
                "4/1;" : [0b1000,0b0100, 0b0010,0b0001],
                "4/2;" : [0b1100,0b0110,0b0011],
                "4/3;" : [0b1110,0b0111],
                "4/4;" : [0b1111],
                "4/1;1;" : [0b1010,0b0101,0b1001],
                "4/2;1;" : [0b1101],
                "4/1;2;" : [0b1011],
                # l = 5
                "5/0;" : [0b00000],
                "5/1;" : [0b10000,0b01000,0b00100,0b00010,0b00001],
                "5/2;" : [0b11000,0b01100,0b00110, 0b00011],
                "5/3;" : [0b11100,0b01110,0b00111],
                "5/4;" : [0b11110,0b01111],
                "5/5;" : [0b11111],
                "5/1;1;" : [0b10100,0b10010,0b10001,0b01010,0b01001,0b00101],
                "5/1;2;" : [0b10011,0b10110,0b01011],
                "5/1;3;" : [0b10111],
                "5/2;1;" : [0b11001,0b11010,0b01101,],
                "5/2;2;" : [0b11011],
                "5/3;1;" : [0b11101],
                "5/1;1;1;" : [0b10101],
            }
    
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
        # TODO: handle cases with a 0 clue
        boolean_statement = ""

        # iterate over row constraints
        for row_idx, row in enumerate(self.nonogram.cells):
            bit_strings = self.possible_d[f"{self.nonogram.columns}/{';'.join(map(str, self.nonogram.row_clues[row_idx]))};"]
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
            bit_strings = self.possible_d[f"{self.nonogram.rows}/{';'.join(map(str, self.nonogram.column_clues[column_idx]))};"]
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
