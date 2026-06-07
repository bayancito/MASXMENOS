from django.urls import path

from . import views

urlpatterns = [

    path(
        '',
        views.reportes,
        name='reportes',
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
