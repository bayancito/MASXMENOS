from django.shortcuts import render, redirect

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