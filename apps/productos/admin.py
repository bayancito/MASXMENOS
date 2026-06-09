from django.contrib import admin
from .models import Categoria, Producto, Solicitud



@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):

    list_display = (
        'nombre',
        'activa',
        'fecha_creacion'
    )

    search_fields = (
        'nombre',
    )

    list_filter = (
        'activa',
    )

@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'comprador',
        'producto',
        'cantidad',
        'estado',
        'fecha_creacion',
    )

    search_fields = (
        'comprador__username',
        'producto__nombre',
    )

    list_filter = (
        'estado',
        'fecha_creacion',
    )


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):


    list_display = (
        'nombre',
        'activo',
        'fecha_creacion'
    )

    search_fields = (
        'nombre',
    )