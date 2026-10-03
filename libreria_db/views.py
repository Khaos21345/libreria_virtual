
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Libro

def inicio(request):
    libros = Libro.objects.all()
    return render(request, 'libreria_db/inicio.html', {'libros': libros})

def crear_libro(request):
    if request.method == 'POST':
        Libro.objects.create(
            titulo=request.POST.get('titulo'),
            autor=request.POST.get('autor'),
            descripcion=request.POST.get('descripcion')
        )
        return redirect('inicio')
    return render(request, 'libreria_db/crear.html')


def detalle_libro(request, id):
    libro = get_object_or_404(Libro, id=id)
    return render(request, 'libreria_db/detalle.html', {'libro': libro})

def editar_libro(request, id):
    libro = get_object_or_404(Libro, id=id)
    if request.method == 'POST':
        libro.titulo = request.POST.get('titulo')
        libro.autor = request.POST.get('autor')
        libro.descripcion = request.POST.get('descripcion')
        libro.disponible = 'disponible' in request.POST
        libro.save()
        return redirect('inicio')
    return render(request, 'libreria_db/editar.html', {'libro': libro})

def eliminar_libro(request, id):
    libro = get_object_or_404(Libro, id=id)
    if request.method == 'POST':
        libro.delete()
        return redirect('inicio')
    return render(request, 'libreria_db/eliminar.html', {'libro': libro})