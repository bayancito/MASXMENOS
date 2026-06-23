from django.contrib import admin

from .models import Incidencia


@admin.register(Incidencia)
class IncidenciaAdmin(admin.ModelAdmin):
    list_display = ("tipo_incidencia", "usuario", "fecha_reporte", "activa")
    list_filter = ("tipo_incidencia", "activa", "fecha_reporte")
    search_fields = ("descripcion", "usuario__username")
