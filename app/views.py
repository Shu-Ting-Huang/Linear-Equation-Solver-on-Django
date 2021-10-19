from app.linear_equation_solver.frontend import output2latex
from app.linear_equation_solver.backend import RowOpSeq
from django.shortcuts import render
from django.http import HttpResponse
import pickle
from sympy import Matrix

# Create your views here.

def index(request):
    if request.method == 'GET':
        return render(request, 'matrix_size_input.html')
    elif request.method == 'POST':
        if request.POST['form_submitted'] == 'matrix_size':
            m = request.session['m'] = int(request.POST['m'])
            n = request.session['n'] = int(request.POST['n'])
            return render(request, 'matrix_input.html', context={'range_m':range(m),'range_n':range(n)})
        elif request.POST['form_submitted'] == 'matrix':
            m = request.session['m']
            n = request.session['n']
            # store the matrix in the variable A
            A = []
            for i in range(m):
                row = []
                for j in range(n):
                    row.append(request.POST.dict()['a_'+str(i)+'_'+str(j)])
                A.append(row)
            # Initialize the row operation sequence
            request.session['row_op_seq'] = pickle.dumps(RowOpSeq(Matrix(A)),0).decode()
            return render(request, 'interactive_row_operations.html')

# Allow the row_ops_iframe.html to be shown in iframe
from django.views.decorators.clickjacking import xframe_options_sameorigin
@xframe_options_sameorigin

def row_ops_iframe(request):
    row_op_seq = pickle.loads(request.session['row_op_seq'].encode())
    return render(request, 'row_ops_iframe.html', context={'row_op':output2latex(row_op_seq)})