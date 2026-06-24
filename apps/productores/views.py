from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)
from django.urls import reverse

from .models import Productor
from .forms import ProductorForm
from apps.productos.models import Categoria

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
    ).prefetch_related(
        'productos__categoria'
    ).annotate(
        num_productos=Count('productos')
    )

    productores_mapa = []

    for productor in productores:
        if not productor.latitud or not productor.longitud:
            continue

        productos = [
            producto
            for producto in productor.productos.all()
            if producto.activo
        ]

        categorias = []
        productos_data = []

        for producto in productos:
            categoria = producto.categoria.nombre if producto.categoria else 'Sin categoria'

            if categoria not in categorias:
                categorias.append(categoria)

            productos_data.append(
                {
                    'id': producto.id,
                    'nombre': producto.nombre,
                    'categoria': categoria,
                    'precio': str(producto.precio),
                }
            )

        productores_mapa.append(
            {
                'id': productor.id,
                'nombre': productor.nombre_comercial,
                'telefono': productor.telefono,
                'direccion': productor.direccion,
                'municipio': productor.municipio,
                'descripcion': productor.descripcion,
                'lat': float(productor.latitud),
                'lng': float(productor.longitud),
                'imagen': productor.imagen_perfil.url if productor.imagen_perfil else '',
                'productos_count': len(productos),
                'productos': productos_data,
                'categorias': categorias,
                'perfil_url': reverse('detalle_productor', args=[productor.id]),
                'activo': productor.activo,
                'tiene_foto': bool(productor.imagen_perfil),
            }
        )

    municipios = Productor.objects.filter(
        activo=True
    ).order_by(
        'municipio'
    ).values_list(
        'municipio',
        flat=True
    ).distinct()

    categorias = Categoria.objects.filter(
        activa=True,
        productos__productor__activo=True,
    ).distinct().order_by('nombre')

    return render(
        request,
        'productores/mapa_productores.html',
        {
            'productores': productores,
            'productores_mapa': productores_mapa,
            'municipios': municipios,
            'categorias': categorias,
        }
    )
