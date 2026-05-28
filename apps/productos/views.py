from django.shortcuts import render, redirect, get_object_or_404

from .forms import ProductoForm
from .models import Producto

def crear_producto(request):

    if request.method == 'POST':

        form = ProductoForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

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

    productos = Producto.objects.all()

    return render(
        request,
        'productos/lista_productos.html',
        {
            'productos': productos
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