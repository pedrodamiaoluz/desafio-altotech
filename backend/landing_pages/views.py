from django.shortcuts import render

# Create your views here.

def sobre_nos(request):
    return render(request, "pages/sobre_nos.html")

def contate_nos(request):
    return render(request, "pages/contate_nos.html")
