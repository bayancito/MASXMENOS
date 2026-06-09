from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Producto, Favorito


@login_required
def agregar_favorito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    Favorito.objects.get_or_create(usuario=request.user, producto=producto)
    return redirect('detalle_producto', pk=producto.id)


@login_required
def mis_favoritos(request):
    favoritos = (
        Favorito.objects.filter(usuario=request.user)
        .select_related('producto')
        .order_by('-fecha_creacion')
    )

    productos = [f.producto for f in favoritos]
    return render(
        request,
        'productos/mis_favoritos.html',
        {
            'productos': productos,
        },
    )

