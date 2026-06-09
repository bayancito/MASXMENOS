from django.urls import path

from .views_favoritos import agregar_favorito, mis_favoritos

urlpatterns = [
    path('favoritos/agregar/<int:producto_id>/', agregar_favorito, name='agregar_favorito'),
    path('favoritos/mis/', mis_favoritos, name='mis_favoritos'),
]

