from django.shortcuts import render, get_object_or_404
from .models import Pelicula
from django.http import JsonResponse
# Create your views here.
def index(request):
    peliculas = Pelicula.objects.all()
    return render(request,'tendencias/index.html',{'peliculas': peliculas})

    
#def detalle(request):
#    return render(request,"core/detalle.html") 
def detalle(request, id):
    pelicula = get_object_or_404(Pelicula, id=id)
    return render(request, 'tendencias/detalle.html', {'pelicula': pelicula})

