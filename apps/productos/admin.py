from django.contrib import admin
from .models import Categoria


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