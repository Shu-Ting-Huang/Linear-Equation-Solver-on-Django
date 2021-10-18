from django.shortcuts import render
from django.http import HttpResponse

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
            request.session['A'] = A
            from .linear_equation_solver import find_solution
            return render(request, 'interactive_row_operations.html')

# Allow the simple_row_ops.html to be shown in iframe
from django.views.decorators.clickjacking import xframe_options_sameorigin
@xframe_options_sameorigin

def simple_row_ops(request):
    print(request.session['A'])
    number_of_steps = int(request.GET['number_of_steps'])
    return render(request, 'simple_row_ops.html', context={'step_range':range(1,number_of_steps+1)})
