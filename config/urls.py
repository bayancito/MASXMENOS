from django.contrib import admin
from django.urls import path, include
from apps.productos.views import dashboard_comprador
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        include('apps.usuarios.urls')
    ),

    path(
        'productos/',
        include('apps.productos.urls')
    ),

    path(
        'productos/solicitudes/',
        include('apps.productos.urls_solicitudes')
    ),

    path(
        'productos/solicitudes-recibidas/',
        include('apps.productos.urls_recibidas')
    ),

    path(
        'productores/',
        include('apps.productores.urls')
    ),

    path(
        'reportes/',
        include('apps.reportes.urls')
    ),

    path(
        'mi-panel/',
        dashboard_comprador,
        name='dashboard_comprador'
    ),

]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )