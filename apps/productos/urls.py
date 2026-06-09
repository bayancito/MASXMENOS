from django.urls import path

from .views import (
    crear_producto,
    lista_productos,
    detalle_producto,
    editar_producto,
    eliminar_producto,
    solicitar_producto,
)


from .urls_favoritos import urlpatterns as favoritos_urls

urlpatterns = favoritos_urls + [
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

    path(
        '<int:pk>/eliminar/',
        eliminar_producto,
        name='eliminar_producto'
    ),

    path(
        '<int:pk>/solicitar/',
        solicitar_producto,
        name='solicitar_producto'
    ),


]