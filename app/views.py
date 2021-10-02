from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    if request.method == 'GET':
        return render(request, 'matrix_size_input.html')
    elif request.method == 'POST':
        if request.POST['form_submitted'] == 'matrix_size':
            global m, n
            m = int(request.POST['m'])
            n = int(request.POST['n'])
            return render(request, 'matrix_input.html', context={'range_m':range(m),'range_n':range(n)})
