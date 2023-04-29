from .algorithm import Algorithm
from ..nonogram import Nonogram
from qiskit import IBMQ, Aer, assemble, transpile, QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit.quantum_info.operators import Operator
from qiskit.providers.ibmq import least_busy
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
    
    def to_boolean_expression(self, nonogram: Nonogram):
        boolean_statement = ""

        for row_idx, row_constraint in enumerate(nonogram.row_constraints):
            bit_strings = self.possible_d[f"{nonogram.rows}/{';'.join(map(str, row_constraint))};"]
            clauses = []
            for bitstring_idx, bitstring in enumerate(bit_strings):
                clause = ""
                for column_idx in range(nonogram.columns):
                    if bitstring & (1 << column_idx):
                        clause += f'v{nonogram.grid_positions[row_idx][column_idx]}&'
                    else:
                        clause += f'~v{nonogram.grid_positions[row_idx][column_idx]}&'
                clauses.append("(" + clause[:-1] + ")")
            boolean_statement += "(" + "|".join(clauses) + ")&"

     # iterate over column constraints (same as with row constraints, but with transposed variables)
        for column_idx, column_constraint in enumerate(nonogram.column_constraints):
            bitstrings = self.possible_d[f"{nonogram.columns}/{';'.join(map(str, column_constraint))};"]
            clauses = []
            for bitstring_idx, bitstring in enumerate(bitstrings):
                clause = ""
                for row_idx in range(nonogram.rows):
                    if bitstring & (1 << row_idx):
                        clause += f"v{nonogram.grid_positions[row_idx][column_idx]}&"
                    else:
                        clause += f"~v{nonogram.grid_positions[row_idx][column_idx]}&"
                clauses.append("(" + clause[:-1] + ")")
            boolean_statement += "(" + "|".join(clauses) + ")&"

        # remove trailing "&" before returning
        return boolean_statement[:-1]
    
    def get_num_iterations(self, nonogram: Nonogram):
        # TODO: Fix assumption that num_solutions = 1
        num_solutions = 1
        return math.ceil(math.pi/4 * math.sqrt(2**(nonogram.rows*nonogram.columns)/num_solutions))

    def solve(self, nonogram: Nonogram):
        circuit = self.make_solver(nonogram)
        backend = Aer.get_backend('aer_simulator')  
        job = execute(circuit, backend, shots=1024)
        result = job.result()
        sorted_counts = dict(sorted(result.get_counts(circuit).items(), key= lambda item: item[1], reverse = True))
        top = dict(list(sorted_counts.items())[:1])
        top_three = dict(list(sorted_counts.items())[:3])
        
        for res in top:
            return red
    
    # TODO: make a "prep" function that isn't involved in timing to set up this
    def make_solver(self, nonogram: Nonogram):
        expression = self.to_boolean_expression(nonogram)
        oracle = PhaseOracle(expression)
        problem = AmplificationProblem(oracle=oracle)
        algorithm = Grover(iterations=self.get_num_iterations(nonogram))
        circuit = algorithm.construct_circuit(problem)
        circuit.measure_all()
        return circuit