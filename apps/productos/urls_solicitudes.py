from django.urls import path

from .views import mis_solicitudes


urlpatterns = [
    path('', mis_solicitudes, name='mis_solicitudes'),
]

