from django.shortcuts import render

from apps.productos.models import Producto, Categoria
from apps.productores.models import Productor


def inicio(request):

    total_productos = Producto.objects.count()
    total_productores = Productor.objects.count()
    total_categorias = Categoria.objects.count()

    productos_activos = Producto.objects.filter(
        activo=True
    ).count()

    productores_activos = Productor.objects.filter(
        activo=True
    ).count()

    ultimos_productos = Producto.objects.order_by(
        '-id'
    )[:5]

    ultimos_productores = Productor.objects.order_by(
        '-id'
    )[:5]

    return render(
        request,
        "inicio.html",
        {
            "total_productos": total_productos,
            "total_productores": total_productores,
            "total_categorias": total_categorias,
            "productos_activos": productos_activos,
            "productores_activos": productores_activos,
            "ultimos_productos": ultimos_productos,
            "ultimos_productores": ultimos_productores,
        },
    )
