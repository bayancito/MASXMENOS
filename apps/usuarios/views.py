from django.shortcuts import render

from apps.productos.models import Producto, Categoria
from apps.productores.models import Productor


def inicio(request):

    total_productos = Producto.objects.count()
    total_productores = Productor.objects.count()
    total_categorias = Categoria.objects.count()

    return render(
        request,
        "inicio.html",
        {
            "total_productos": total_productos,
            "total_productores": total_productores,
            "total_categorias": total_categorias,
        },
    )
