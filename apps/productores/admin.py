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
        'municipio'
    )