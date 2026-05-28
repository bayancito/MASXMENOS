from django.urls import path

from .views import (
    crear_producto,
    lista_productos,
    detalle_producto,
    editar_producto
)

urlpatterns = [

    path(
        '',
        lista_productos,
        name='lista_productos'
    ),

    path(
        'nuevo/',
        crear_producto,
        name='crear_producto'
    ),

     path(
        '<int:pk>/',
        detalle_producto,
        name='detalle_producto'
    ),

    path(
        '<int:pk>/editar/',
        editar_producto,
        name='editar_producto'
    ),

]