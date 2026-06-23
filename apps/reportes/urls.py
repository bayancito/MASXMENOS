from django.urls import path

from . import views

urlpatterns = [

    path(
        '',
        views.reportes,
        name='reportes',
    ),

    path(
        'incidencias/',
        views.incidencia_list,
        name='incidencias_list',
    ),

    path(
        'incidencias/nueva/',
        views.crear_incidencia,
        name='incidencias_nueva',
    ),

    path(
        'excel/productos/',
        views.exportar_productos_excel,
        name='excel_productos'
    ),

    path(
        'excel/productores/',
        views.exportar_productores_excel,
        name='excel_productores'
    ),

    path(
        'pdf/',
        views.exportar_pdf,
        name='exportar_pdf'
    ),

]
