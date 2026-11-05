from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_pagina, name='login_pagina'),
    path('libros/', views.inicio, name='inicio'),
    path('crear/', views.crear_libro, name="crear_libro"),
    path('detalle/<int:id>/', views.detalle_libro, name='detalle_libro'),
    path('editar/<int:id>/', views.editar_libro, name='editar_libro'), 
    path('eliminar/<int:id>/', views.eliminar_libro, name='eliminar_libro'),

    path('api/login/', views.LoginApiView.as_view(), name='login_api'),

    path('api/libros/', views.librosApiView.as_view(), name="api_libros"),

    path('api/libros/<int:id>/', views.LibroDetalleApiView.as_view(), name="api_libro_detalle"),
]