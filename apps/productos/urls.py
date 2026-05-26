from django.urls import path

from .views import crear_producto


urlpatterns = [

    path(
        'nuevo/',
        crear_producto,
        name='crear_producto'
    ),

]