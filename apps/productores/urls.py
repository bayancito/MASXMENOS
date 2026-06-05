from django.urls import path

from .views import (
    lista_productores,
    detalle_productor,
    crear_productor,
    editar_productor,
    eliminar_productor
)

urlpatterns = [

    path(
        '',
        lista_productores,
        name='lista_productores'
    ),

    path(
        'nuevo/',
        crear_productor,
        name='crear_productor'
    ),

    path(
        '<int:pk>/',
        detalle_productor,
        name='detalle_productor'
    ),

    path(
        '<int:pk>/editar/',
        editar_productor,
        name='editar_productor'
    ),
    path(
    '<int:pk>/eliminar/',
    eliminar_productor,
    name='eliminar_productor'
    ),

]