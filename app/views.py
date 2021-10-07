from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    if request.method == 'GET':
        return render(request, 'matrix_size_input.html')
    elif request.method == 'POST':
        if request.POST['form_submitted'] == 'matrix_size':
            m = int(request.POST['m'])
            n = int(request.POST['n'])
            return render(request, 'matrix_input.html', context={'range_m':range(m),'range_n':range(n),'m':m,'n':n})
        elif request.POST['form_submitted'] == 'matrix':
            m = int(request.POST['m'])
            n = int(request.POST['n'])
            # store the matrix in the variable A
            A = []
            for i in range(m):
                row = []
                for j in range(n):
                    row.append(request.POST.dict()['a_'+str(i)+'_'+str(j)])
                A.append(row)
            from .linear_equation_solver import find_solution
            return render(request, 'display_row_operations.html', context={'row_op':find_solution(A)})
