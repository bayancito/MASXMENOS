from django.urls import path

from .views import (
    crear_producto,
    lista_productos
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

]