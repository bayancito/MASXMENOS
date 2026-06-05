from django.db.models import Count
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)

from .models import Productor
from .forms import ProductorForm


def lista_productores(request):

    productores = Productor.objects.annotate(
        num_productos=Count('productos')
    )

    return render(
        request,
        'productores/lista_productores.html',
        {
            'productores': productores,
        }
    )


def detalle_productor(request, pk):

    productor = get_object_or_404(
        Productor.objects.prefetch_related(
            'productos__categoria'
        ),
        pk=pk,
    )

    return render(
        request,
        'productores/detalle_productor.html',
        {
            'productor': productor,
        }
    )


def crear_productor(request):

    if request.method == 'POST':

        form = ProductorForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect(
                'lista_productores'
            )

    else:

        form = ProductorForm()

    return render(
        request,
        'productores/crear_productor.html',
        {
            'form': form
        }
    )

def editar_productor(request, pk):

    productor = get_object_or_404(
        Productor,
        pk=pk
    )

    if request.method == 'POST':

        form = ProductorForm(
            request.POST,
            instance=productor
        )

        if form.is_valid():

            form.save()

            return redirect(
                'detalle_productor',
                pk=productor.pk
            )

    else:

        form = ProductorForm(
            instance=productor
        )

    return render(
        request,
        'productores/editar_productor.html',
        {
            'form': form,
            'productor': productor
        }
    )

def eliminar_productor(request, pk):

    productor = get_object_or_404(
        Productor,
        pk=pk
    )

    if request.method == 'POST':

        productor.delete()

        return redirect(
            'lista_productores'
        )

    return render(
        request,
        'productores/eliminar_productor.html',
        {
            'productor': productor
        }
    )