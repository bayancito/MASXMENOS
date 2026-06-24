from django.contrib import admin
from .models import Categoria, Producto, ProductoImagen, Solicitud, Cosecha, ContactoProducto, SolicitudCompra




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
        'productor',
        'producto',
        'cantidad',
        'estado',
        'fecha_creacion',
    )

    search_fields = (
        'comprador__username',
        'productor__nombre_comercial',
        'producto__nombre',
    )

    list_filter = (
        'estado',
        'fecha_creacion',
    )


@admin.register(ContactoProducto)
class ContactoProductoAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'comprador',
        'productor',
        'producto',
        'canal',
        'fecha_creacion',
    )

    search_fields = (
        'comprador__username',
        'productor__nombre_comercial',
        'producto__nombre',
        'mensaje',
    )

    list_filter = (
        'canal',
        'fecha_creacion',
    )


@admin.register(SolicitudCompra)
class SolicitudCompraAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'comprador',
        'productor',
        'producto',
        'cantidad_solicitada',
        'estado',
        'fecha_creacion',
    )

    search_fields = (
        'comprador__username',
        'productor__nombre_comercial',
        'producto__nombre',
        'mensaje_adicional',
    )

    list_filter = (
        'estado',
        'fecha_creacion',
    )


class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 1


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):

    list_display = (
        'nombre',
        'categoria',
        'precio',
        'activo',
        'fecha_creacion'
    )

    search_fields = (
        'nombre',
        'descripcion',
    )

    list_filter = (
        'activo',
        'categoria',
        'fecha_creacion',
    )

    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'descripcion', 'categoria')
        }),
        ('Precio y disponibilidad', {
            'fields': ('precio', 'activo')
        }),
        ('Multimedia', {
            'fields': ('imagen',)
        }),
        ('Productor', {
            'fields': ('productor',)
        }),
    )

    inlines = [
        ProductoImagenInline,
    ]


@admin.register(Cosecha)
class CosechaAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'producto',
        'productor',
        'cantidad',
        'unidad_medida',
        'precio_esperado',
        'fecha_cosecha',
        'estado',
        'fecha_creacion',
    )

    search_fields = (
        'producto__nombre',
        'productor__username',
    )

    list_filter = (
        'estado',
        'fecha_cosecha',
    )

