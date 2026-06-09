from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)

from .models import Productor
from .forms import ProductorForm

from apps.usuarios.decorators import es_productor_o_admin






def lista_productores(request):

    busqueda = request.GET.get(
        'q',
        ''
    )

    municipio = request.GET.get(
        'municipio',
        ''
    )

    productores = Productor.objects.annotate(
        num_productos=Count('productos')
    )

    if busqueda:

        productores = productores.filter(
            Q(nombre_comercial__icontains=busqueda)
            | Q(municipio__icontains=busqueda)
            | Q(telefono__icontains=busqueda)
        )

    if municipio:

        productores = productores.filter(
            municipio=municipio
        )

    municipios = Productor.objects.order_by(
        'municipio'
    ).values_list(
        'municipio',
        flat=True
    ).distinct()

    paginator = Paginator(
        productores,
        10
    )

    page_number = request.GET.get('page')

    productores = paginator.get_page(
        page_number
    )

    return render(
        request,
        'productores/lista_productores.html',
        {
            'productores': productores,
            'busqueda': busqueda,
            'municipios': municipios,
            'municipio_seleccionado': municipio,
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


from apps.usuarios.decorators import es_productor_o_admin


@es_productor_o_admin
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

@es_productor_o_admin
def editar_productor(request, pk):


    productor = get_object_or_404(
        Productor,
        pk=pk
    )

    rol = request.user.perfil.rol

    if rol != "ADMIN" and productor.usuario != request.user:
        return redirect("lista_productores")


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

    rol = request.user.perfil.rol

    if rol != "ADMIN" and productor.usuario != request.user:
        return redirect("lista_productores")


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


def mapa_productores(request):

    productores = Productor.objects.filter(
        activo=True
    )

    return render(
        request,
        'productores/mapa_productores.html',
        {
            'productores': productores
        }
    )