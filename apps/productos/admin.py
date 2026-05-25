from django.contrib import admin
from .models import Categoria , Producto


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