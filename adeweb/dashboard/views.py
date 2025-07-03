from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from memory_profiler import profile

@profile
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

