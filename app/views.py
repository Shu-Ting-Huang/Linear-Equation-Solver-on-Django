from app.linear_equation_solver.frontend import output2latex
from app.linear_equation_solver.backend import RowOpSeq
from django.shortcuts import render
from django.http import HttpResponse
import pickle
from sympy import Matrix, Rational

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
            return render(request, 'interactive_row_operations.html',context={'range_m':range(m)})

# Allow the row_ops_iframe.html to be shown in iframe
from django.views.decorators.clickjacking import xframe_options_sameorigin
@xframe_options_sameorigin

def row_ops_iframe(request):
    row_op_seq = pickle.loads(request.session['row_op_seq'].encode())
    if request.GET.dict() != {}: # if query string parameters are non-empty
        if request.GET["op"] == "n<->m":
            next_row_op = {}
            next_row_op["op"] = "n<->m"
            next_row_op["row1"] = int(request.GET["row1"])
            next_row_op["row2"] = int(request.GET["row2"])
            row_op_seq.add_step(next_row_op)
            del next_row_op
        if request.GET["op"] == "n->n km": # "+" becomes " " when passed as query string parameters
            next_row_op = {}
            next_row_op["op"] = "n->n+km"
            next_row_op["row"] = int(request.GET["row"])
            next_row_op["row2"] = int(request.GET["row2"])
            next_row_op["k"] = Rational(request.GET["k"])
            row_op_seq.add_step(next_row_op)
            del next_row_op
        if request.GET["op"] == "undo":
            row_op_seq.undo()
        request.session['row_op_seq'] = pickle.dumps(row_op_seq,0).decode()
    return render(request, 'row_ops_iframe.html', context={'row_op':output2latex(row_op_seq)})