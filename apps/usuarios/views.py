from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.productos.models import Producto, Categoria
from apps.productores.models import Productor

from .forms import RegistroForm, PerfilForm


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


def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegistroForm()

    return render(
        request,
        "usuarios/registro.html",
        {"form": form},
    )


@login_required
def perfil_usuario(request):
    # Asegura que el perfil exista (evita RelatedObjectDoesNotExist)
    try:
        perfil = request.user.perfil
    except Exception:
        perfil = None
        try:
            from .models import Perfil
            perfil, _ = Perfil.objects.get_or_create(user=request.user)
        except Exception:
            # Si por alguna razón falla la creación, se re-lanza el error original
            raise

    if request.method == "POST":
        form = PerfilForm(
            request.POST,
            request.FILES,
            instance=perfil,
        )
        if form.is_valid():
            form.save()
            return redirect("perfil")
    else:
        form = PerfilForm(instance=perfil)

    return render(
        request,
        "usuarios/perfil.html",
        {
            "perfil": perfil,
            "form": form,
        },
    )
