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


def _rol_usuario(user):
    if not user.is_authenticated:
        return None

    perfil = getattr(user, 'perfil', None)
    return getattr(perfil, 'rol', None)


def _puede_crear_productor(user, rol):
    if rol == 'ADMIN':
        return True

    if rol == 'PRODUCTOR':
        return not Productor.objects.filter(usuario=user).exists()

    return False






def lista_productores(request):

    busqueda = request.GET.get(
        'q',
        ''
    )

    municipio = request.GET.get(
        'municipio',
        ''
    )

    orden = request.GET.get(
        'orden',
        'nombre'
    )

    productores = Productor.objects.annotate(
        num_productos=Count('productos')
    ).select_related('usuario')

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

    if orden == 'recientes':
        productores = productores.order_by('-fecha_creacion')
    elif orden == 'productos':
        productores = productores.order_by('-num_productos', 'nombre_comercial')
    else:
        productores = productores.order_by('nombre_comercial')

    municipios = Productor.objects.order_by(
        'municipio'
    ).values_list(
        'municipio',
        flat=True
    ).distinct()

    paginator = Paginator(
        productores,
        8
    )

    page_number = request.GET.get('page')

    productores = paginator.get_page(
        page_number
    )

    rol_usuario = _rol_usuario(request.user)

    return render(
        request,
        'productores/lista_productores.html',
        {
            'productores': productores,
            'busqueda': busqueda,
            'municipios': municipios,
            'municipio_seleccionado': municipio,
            'orden_seleccionado': orden,
            'rol_usuario': rol_usuario,
            'puede_crear_productor': _puede_crear_productor(
                request.user,
                rol_usuario
            ),
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


@es_productor_o_admin
def crear_productor(request):

    if request.method == 'POST':

        form = ProductorForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            productor = form.save(commit=False)

            if request.user.perfil.rol != 'ADMIN':
                productor.usuario = request.user

            productor.save()

            return redirect(
                'lista_productores'
            )

    else:

        form = ProductorForm()

    return render(
        request,
        'productores/crear_productor.html',
        {
            'form': form,
            'modo_formulario': 'crear'
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
            request.FILES,
            instance=productor
        )

        if form.is_valid():

            productor = form.save(commit=False)

            if rol != 'ADMIN':
                productor.usuario = request.user

            productor.save()

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
            'productor': productor,
            'modo_formulario': 'editar'
        }
    )

@es_productor_o_admin
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
