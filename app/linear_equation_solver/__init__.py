from .frontend import *
from .backend import *
from sympy import Matrix

find_solution = lambda A: output2latex(row_op_toward_RREF(Matrix(A)))