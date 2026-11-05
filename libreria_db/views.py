from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status

from .models import Libro
from .forms import LibroForm


def inicio(request):
    libros = Libro.objects.all()
    return render(request, "libreria_db/inicio.html", {"libros": libros})

@login_required
def crear_libro(request):
    if request.method == "POST":
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inicio")
    else:
        form = LibroForm()
    return render(request, "libreria_db/crear.html", {"form": form})

def detalle_libro(request, id):
    libro = get_object_or_404(Libro, id=id)
    return render(request, "libreria_db/detalle.html", {"libro": libro})

@login_required
def editar_libro(request, id):
    libro = get_object_or_404(Libro, id=id)
    if request.method == "POST":
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            return redirect("inicio")
    else:
        form = LibroForm(instance=libro)
    return render(request, "libreria_db/editar.html", {"form": form, "libro": libro})

@login_required
def eliminar_libro(request, id):
    libro = get_object_or_404(Libro, id=id)
    if request.method == "POST":
        libro.delete()
        return redirect("inicio")
    return render(request, "libreria_db/eliminar.html", {"libro": libro})

def login_pagina(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Autenticar usuario con Django
        usuario = authenticate(request, username=username, password=password)
        
        if usuario is not None:
            login(request, usuario)  # Crea la sesión en el navegador
            return redirect('inicio')  # Te redirige a la vista de tus libros
        else:
            return render(request, 'libreria_db/login.html', {'error': True})
            
    return render(request, 'libreria_db/login.html')


class LoginApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        usuario = authenticate(username=username, password=password)

        if usuario is not None:
            token, creado = Token.objects.get_or_create(user=usuario)
            return Response({
                'mensaje': 'Autenticacion Correcta',
                'usuario': usuario.username,
                'token': token.key
            }, status=status.HTTP_200_OK)

        return Response({
            'error': 'usuario o contraseña incorrectos'
        }, status=status.HTTP_401_UNAUTHORIZED)


class librosApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        libros = Libro.objects.all()
        datos = []
        for libro in libros:
            datos.append({
                'id': libro.id,
                'titulo': libro.titulo,
                'autor': libro.autor,
                'descripcion': libro.descripcion,
                'disponible': libro.disponible
            })
        return Response(datos, status=status.HTTP_200_OK)

    def post(self, request):
        titulo = request.data.get('titulo')
        autor = request.data.get('autor')
        descripcion = request.data.get('descripcion', '')
        disponible = request.data.get('disponible', True)

        if not titulo or not autor:
            return Response({'error': 'Título y autor son obligatorios'}, status=status.HTTP_400_BAD_REQUEST)

        libro = Libro.objects.create(
            titulo=titulo,
            autor=autor,
            descripcion=descripcion,
            disponible=disponible
        )
        return Response({
            'mensaje': 'Libro creado correctamente',
            'id': libro.id
        }, status=status.HTTP_201_CREATED)


class LibroDetalleApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        libro = get_object_or_404(Libro, id=id)
        return Response({
            'id': libro.id,
            'titulo': libro.titulo,
            'autor': libro.autor,
            'descripcion': libro.descripcion,
            'disponible': libro.disponible
        }, status=status.HTTP_200_OK)

    def put(self, request, id):
        libro = get_object_or_404(Libro, id=id)
        titulo = request.data.get('titulo')
        autor = request.data.get('autor')
        descripcion = request.data.get('descripcion')
        disponible = request.data.get('disponible')

        if titulo is None or autor is None or disponible is None:
            return Response({
                'error': 'Debes enviar todos los campos obligatorios'
            }, status=status.HTTP_400_BAD_REQUEST)

        libro.titulo = titulo
        libro.autor = autor
        libro.descripcion = descripcion
        libro.disponible = disponible
        libro.save()

        return Response({
            'mensaje': 'Libro actualizado correctamente',
            'id': libro.id,
            'titulo': libro.titulo,
            'autor': libro.autor,
            'descripcion': libro.descripcion,
            'disponible': libro.disponible
        }, status=status.HTTP_200_OK)

    def delete(self, request, id):
        libro = get_object_or_404(Libro, id=id)
        libro.delete()
        return Response({
            'mensaje': 'Libro eliminado correctamente'
        }, status=status.HTTP_204_NO_CONTENT)