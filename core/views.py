from django.shortcuts import render,HttpResponse

# Create your views here.

def registrarse(request):
    return render(request,"core/registrarse.html")
def login(request):
    return render(request,"core/iniciosesion.html")