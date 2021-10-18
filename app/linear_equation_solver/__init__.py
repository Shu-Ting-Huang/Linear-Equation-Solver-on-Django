from .frontend import *
from .backend import *
from sympy import Matrix

row_op_step_num = lambda A: len(row_op_toward_RREF(Matrix(A)).row_op_seq)

def find_solution(A, number_of_steps = None):
    if number_of_steps == None:
        number_of_steps = row_op_step_num(A)
    return output2latex(row_op_toward_RREF(Matrix(A)), number_of_steps=number_of_steps)

# find_solution = lambda A: output2latex(row_op_toward_RREF(Matrix(A)))