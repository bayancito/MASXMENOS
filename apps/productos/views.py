from django.shortcuts import render, redirect, get_object_or_404

from apps.usuarios.decorators import es_productor_o_admin

from .forms import ProductoForm
from .models import Producto, Categoria, Favorito

from django.core.paginator import Paginator

@es_productor_o_admin
def crear_producto(request):


    if request.method == 'POST':
        form = ProductoForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            producto = form.save(commit=False)

            if hasattr(request.user, 'productor'):
                producto.productor = request.user.productor

            producto.save()

            return redirect('/')

    else:

        form = ProductoForm()

    return render(
        request,
        'productos/crear_producto.html',
        {
            'form': form
        }
    )
def lista_productos(request):

    busqueda = request.GET.get(
        'q',
        ''
    )

    categoria_id = request.GET.get(
        'categoria',
        ''
    )

    productos = Producto.objects.all()

    if busqueda:

        productos = productos.filter(
            nombre__icontains=busqueda
        )

    if categoria_id:

        productos = productos.filter(
            categoria_id=categoria_id
        )

    categorias = Categoria.objects.all()
    paginator = Paginator(
            productos,
            10
        )

    page_number = request.GET.get('page')

    productos = paginator.get_page(
            page_number
        )

    return render(
        request,
        'productos/lista_productos.html',
        {
            'productos': productos,
            'busqueda': busqueda,
            'categorias': categorias,
            'categoria_seleccionada': categoria_id
        }
    )


def detalle_producto(request, pk):

    producto = get_object_or_404(
        Producto,
        pk=pk
    )

    return render(
        request,
        'productos/detalle_producto.html',
        {
            'producto': producto
        }
    )
def editar_producto(request, pk):

    producto = get_object_or_404(
        Producto,
        pk=pk
    )

    if request.user.is_authenticated and hasattr(request.user, "perfil"):
        rol = request.user.perfil.rol
        if rol != "ADMIN":
            # Permitir solo si el productor del producto pertenece al usuario logueado
            if not (hasattr(producto, "productor") and producto.productor.usuario == request.user):
                return redirect("lista_productos")

    if request.method == 'POST':
        form = ProductoForm(
            request.POST,
            request.FILES,
            instance=producto
        )

        if form.is_valid():

            form.save()

            return redirect(
                'detalle_producto',
                pk=producto.pk
            )

    else:

        form = ProductoForm(
            instance=producto
        )

    return render(
        request,
        'productos/editar_producto.html',
        {
            'form': form,
            'producto': producto
        }
    )

@es_productor_o_admin
def eliminar_producto(request, pk):

    producto = get_object_or_404(
        Producto,
        pk=pk
    )

    if request.user.is_authenticated and hasattr(request.user, "perfil"):
        rol = request.user.perfil.rol
        if rol != "ADMIN":
            if not (hasattr(producto, "productor") and producto.productor.usuario == request.user):
                return redirect("lista_productos")


    if request.method == 'POST':

        producto.delete()

        return redirect(
            'lista_productos'
        )

    return render(
        request,
        'productos/eliminar_producto.html',
        {
            'producto': producto
        }
    )