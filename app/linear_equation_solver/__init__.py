from .frontend import *
from .backend import *
from sympy import Matrix

find_solution = lambda A: output2latex(find_RREF(Matrix(A)))