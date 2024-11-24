from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def contratación(request):
    return render(request, 'contratación.html')
