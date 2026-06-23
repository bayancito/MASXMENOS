from django.contrib import admin
from .models import Productor


@admin.register(Productor)
class ProductorAdmin(admin.ModelAdmin):

    list_display = (
        'nombre_comercial',
        'telefono',
        'municipio',
        'activo'
    )

    search_fields = (
        'nombre_comercial',
        'municipio',
        'descripcion'
    )

    list_filter = (
        'activo',
        'municipio'
    )

    fieldsets = (
        ('Informacion principal', {
            'fields': ('usuario', 'nombre_comercial', 'telefono', 'municipio', 'direccion')
        }),
        ('Perfil publico', {
            'fields': ('descripcion', 'imagen_perfil', 'activo')
        }),
        ('Ubicacion', {
            'fields': ('latitud', 'longitud')
        }),
    )
