from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

from apps.usuarios.decorators import es_productor_o_admin

from .forms import ProductoForm, SolicitudForm, CosechaForm
from .models import Producto, Categoria, Favorito, Solicitud, Cosecha


@es_productor_o_admin
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)

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
            'form': form,
        }
    )


def lista_productos(request):
    busqueda = request.GET.get('q', '')
    categoria_id = request.GET.get('categoria', '')

    productos = Producto.objects.all()

    if busqueda:
        productos = productos.filter(nombre__icontains=busqueda)

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    categorias = Categoria.objects.all()
    paginator = Paginator(productos, 10)

    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)

    return render(
        request,
        'productos/lista_productos.html',
        {
            'productos': productos,
            'busqueda': busqueda,
            'categorias': categorias,
            'categoria_seleccionada': categoria_id,
        },
    )


def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    return render(
        request,
        'productos/detalle_producto.html',
        {
            'producto': producto,
        },
    )


def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.user.is_authenticated and hasattr(request.user, "perfil"):
        rol = request.user.perfil.rol
        if rol != "ADMIN":
            if not (hasattr(producto, "productor") and producto.productor.usuario == request.user):
                return redirect("lista_productos")

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)

        if form.is_valid():
            form.save()
            return redirect('detalle_producto', pk=producto.pk)
    else:
        form = ProductoForm(instance=producto)

    return render(
        request,
        'productos/editar_producto.html',
        {
            'form': form,
            'producto': producto,
        },
    )


@es_productor_o_admin
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.user.is_authenticated and hasattr(request.user, "perfil"):
        rol = request.user.perfil.rol
        if rol != "ADMIN":
            if not (hasattr(producto, "productor") and producto.productor.usuario == request.user):
                return redirect("lista_productos")

    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')

    return render(
        request,
        'productos/eliminar_producto.html',
        {
            'producto': producto,
        },
    )


def mis_solicitudes(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if not hasattr(request.user, 'perfil') or request.user.perfil.rol != 'COMPRADOR':
        return redirect('inicio')

    solicitudes = Solicitud.objects.filter(comprador=request.user).order_by('-fecha_creacion')

    return render(
        request,
        'productos/mis_solicitudes.html',
        {
            'solicitudes': solicitudes,
        },
    )


def solicitudes_recibidas(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if not hasattr(request.user, 'perfil') or request.user.perfil.rol != 'PRODUCTOR':
        return redirect('inicio')

    solicitudes = Solicitud.objects.filter(
        producto__productor__usuario=request.user
    ).order_by('-fecha_creacion')

    return render(
        request,
        'productos/solicitudes_recibidas.html',
        {
            'solicitudes': solicitudes,
        },
    )


def dashboard_productor(request):
    if not request.user.is_authenticated:
        return redirect('inicio')

    if not hasattr(request.user, 'perfil') or request.user.perfil.rol != 'PRODUCTOR':
        return redirect('inicio')

    total_productos = Producto.objects.filter(
        productor__usuario=request.user
    ).count()

    solicitudes_pendientes = Solicitud.objects.filter(
        producto__productor__usuario=request.user,
        estado=Solicitud.PENDIENTE
    ).count()

    solicitudes_aceptadas = Solicitud.objects.filter(
        producto__productor__usuario=request.user,
        estado=Solicitud.ACEPTADA
    ).count()

    solicitudes_rechazadas = Solicitud.objects.filter(
        producto__productor__usuario=request.user,
        estado=Solicitud.RECHAZADA
    ).count()

    ultimas_solicitudes = Solicitud.objects.filter(
        producto__productor__usuario=request.user
    ).order_by('-fecha_creacion')[:5]

    return render(
        request,
        'productos/dashboard_productor.html',
        {
            'total_productos': total_productos,
            'solicitudes_pendientes': solicitudes_pendientes,
            'solicitudes_aceptadas': solicitudes_aceptadas,
            'solicitudes_rechazadas': solicitudes_rechazadas,
            'ultimas_solicitudes': ultimas_solicitudes,
        }
    )


@require_POST
def aceptar_solicitud(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    if not hasattr(request.user, 'perfil') or request.user.perfil.rol != 'PRODUCTOR':
        return redirect('inicio')

    solicitud = get_object_or_404(Solicitud, pk=pk)

    if solicitud.producto.productor is None or solicitud.producto.productor.usuario != request.user:
        return redirect('inicio')

    solicitud.estado = Solicitud.ACEPTADA
    solicitud.save()

    return redirect('solicitudes_recibidas')


@require_POST
def rechazar_solicitud(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    if not hasattr(request.user, 'perfil') or request.user.perfil.rol != 'PRODUCTOR':
        return redirect('inicio')

    solicitud = get_object_or_404(Solicitud, pk=pk)

    if solicitud.producto.productor is None or solicitud.producto.productor.usuario != request.user:
        return redirect('inicio')

    solicitud.estado = Solicitud.RECHAZADA
    solicitud.save()

    return redirect('solicitudes_recibidas')


def dashboard_comprador(request):
    if not request.user.is_authenticated:
        return redirect('inicio')

    if not hasattr(request.user, 'perfil') or request.user.perfil.rol != 'COMPRADOR':
        return redirect('inicio')

    total_favoritos = Favorito.objects.filter(usuario=request.user).count()
    total_solicitudes = Solicitud.objects.filter(comprador=request.user).count()

    solicitudes_pendientes = Solicitud.objects.filter(
        comprador=request.user,
        estado=Solicitud.PENDIENTE
    ).count()

    solicitudes_aceptadas = Solicitud.objects.filter(
        comprador=request.user,
        estado=Solicitud.ACEPTADA
    ).count()

    ultimas_solicitudes = Solicitud.objects.filter(
        comprador=request.user
    ).order_by('-fecha_creacion')[:5]

    return render(
        request,
        'usuarios/dashboard_comprador.html',
        {
            'total_favoritos': total_favoritos,
            'total_solicitudes': total_solicitudes,
            'solicitudes_pendientes': solicitudes_pendientes,
            'solicitudes_aceptadas': solicitudes_aceptadas,
            'ultimas_solicitudes': ultimas_solicitudes,
        }
    )


def _get_cosecha_owner_or_403(request, cosecha):
    """
    Retorna la cosecha si el usuario es propietario; si no, 403.
    """
    if not request.user.is_authenticated or not hasattr(request.user, "perfil"):
        return None

    rol = request.user.perfil.rol
    if rol != "PRODUCTOR":
        return None

    if cosecha.productor != request.user:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("No tienes permiso para acceder a esta cosecha.")

    return None


def crear_cosecha(request):
    if not request.user.is_authenticated or not hasattr(request.user, "perfil"):
        return redirect('inicio')

    if request.user.perfil.rol != "PRODUCTOR":
        return redirect('inicio')

    if request.method == "POST":
        form = CosechaForm(request.POST, request.FILES)
        if form.is_valid():
            cosecha = form.save(commit=False)
            cosecha.productor = request.user
            cosecha.save()
            return redirect("mis_cosechas")
    else:
        form = CosechaForm()

    return render(
        request,
        "productos/cosecha_form.html",
        {
            "form": form,
        },
    )


def mis_cosechas(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if not hasattr(request.user, "perfil") or request.user.perfil.rol != "PRODUCTOR":
        return redirect('inicio')

    cosechas = Cosecha.objects.filter(productor=request.user).order_by("-fecha_creacion")

    return render(
        request,
        "productos/cosecha_list.html",
        {
            "cosechas": cosechas,
        },
    )


def editar_cosecha(request, pk):
    cosecha = get_object_or_404(Cosecha, pk=pk)

    if not request.user.is_authenticated or not hasattr(request.user, "perfil"):
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("No autorizado.")

    if request.user.perfil.rol != "PRODUCTOR" or cosecha.productor != request.user:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("No tienes permiso para editar esta cosecha.")

    if request.method == "POST":
        form = CosechaForm(request.POST, request.FILES, instance=cosecha)
        if form.is_valid():
            form.save()
            return redirect("mis_cosechas")
    else:
        form = CosechaForm(instance=cosecha)

    return render(
        request,
        "productos/cosecha_form.html",
        {
            "form": form,
            "cosecha": cosecha,
        },
    )


def eliminar_cosecha(request, pk):
    cosecha = get_object_or_404(Cosecha, pk=pk)

    if not request.user.is_authenticated or not hasattr(request.user, "perfil"):
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("No autorizado.")

    if request.user.perfil.rol != "PRODUCTOR" or cosecha.productor != request.user:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("No tienes permiso para eliminar esta cosecha.")

    if request.method == "POST":
        cosecha.delete()
        return redirect("mis_cosechas")

    # No existe plantilla de confirmación en el repo; evita error por template faltante.


def solicitar_producto(request, pk):
    # VISITANTE: redirigir a login si intenta comprar
    if not request.user.is_authenticated or not hasattr(request.user, "perfil"):
        return redirect('login')

    # COMPRADOR solamente
    if request.user.perfil.rol != "COMPRADOR":
        return redirect('login')

    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        form = SolicitudForm(request.POST)

        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.comprador = request.user
            solicitud.producto = producto
            solicitud.estado = Solicitud.PENDIENTE
            solicitud.save()
            return redirect('detalle_producto', pk=pk)
    else:
        form = SolicitudForm()

    return render(
        request,
        'productos/solicitar_producto.html',
        {
            'producto': producto,
            'form': form,
        },
    )

