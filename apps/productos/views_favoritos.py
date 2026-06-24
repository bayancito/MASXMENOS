from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User  # noqa: F401 (se mantiene por compatibilidad)
from apps.usuarios.decorators import es_comprador

from .models import Producto, Favorito


@es_comprador
def agregar_favorito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    Favorito.objects.get_or_create(usuario=request.user, producto=producto)
    return redirect('detalle_producto', pk=producto.id)


@es_comprador
def mis_favoritos(request):
    favoritos = (
        Favorito.objects.filter(usuario=request.user)
        .select_related(
            'producto',
            'producto__categoria',
            'producto__productor',
        )
        .prefetch_related('producto__imagenes')
        .order_by('-fecha_creacion')
    )

    return render(
        request,
        'productos/mis_favoritos.html',
        {
            'favoritos': favoritos,
        },
    )

