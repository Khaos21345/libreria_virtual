from django.shortcuts import render, redirect, get_object_or_404
from .models import Libro
from .forms import LibroForm


def inicio(request):
    libros = Libro.objects.all()
    return render(
        request,
        "libreria_db/inicio.html",
        {"libros": libros},
    )


def crear_libro(request):
    if request.method == "POST":
        form = LibroForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("inicio")
    else:
        form = LibroForm()

    return render(
        request,
        "libreria_db/crear.html",
        {"form": form},
    )


def detalle_libro(request, id):
    libro = get_object_or_404(Libro, id=id)
    return render(
        request,
        "libreria_db/detalle.html",
        {"libro": libro},
    )


def editar_libro(request, id):
    libro = get_object_or_404(Libro, id=id)

    if request.method == "POST":
        form = LibroForm(request.POST, instance=libro)

        if form.is_valid():
            form.save()
            return redirect("inicio")
    else:
        form = LibroForm(instance=libro)

    return render(
        request,
        "libreria_db/editar.html",
        {"form": form, "libro": libro},
    )


def eliminar_libro(request, id):
    libro = get_object_or_404(Libro, id=id)

    if request.method == "POST":
        libro.delete()
        return redirect("inicio")

    return render(
        request,
        "libreria_db/eliminar.html",
        {"libro": libro},
    )