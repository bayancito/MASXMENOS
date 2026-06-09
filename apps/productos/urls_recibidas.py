from django.urls import path

from .views import solicitudes_recibidas, aceptar_solicitud, rechazar_solicitud


urlpatterns = [
    path('', solicitudes_recibidas, name='solicitudes_recibidas'),
    path('solicitudes/<int:pk>/aceptar/', aceptar_solicitud, name='aceptar_solicitud'),
    path('solicitudes/<int:pk>/rechazar/', rechazar_solicitud, name='rechazar_solicitud'),
]


