from django.shortcuts import render

def profiler_app(request):
    return render(request, 'home.html')
