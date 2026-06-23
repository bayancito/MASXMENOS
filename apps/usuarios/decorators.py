import functools

from django.shortcuts import redirect


def _get_rol(request):
    perfil = getattr(request.user, "perfil", None)
    return getattr(perfil, "rol", None)


def _redirect_login_if_not_authenticated(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return None


def es_admin(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and _get_rol(request) == "ADMIN":
            return view_func(request, *args, **kwargs)
        # Para mantener compatibilidad: cualquier denegación va a inicio
        return redirect("inicio")

    return wrapper


def es_productor_o_admin(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        rol = _get_rol(request)
        if rol in ["ADMIN", "PRODUCTOR"]:
            return view_func(request, *args, **kwargs)

        return redirect("inicio")

    return wrapper


def es_comprador(view_func):
    """
    COMPRADOR:
    - Si no está autenticado => redirect('login')
    - Si el rol no es COMPRADOR => redirect('inicio')
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        redir = _redirect_login_if_not_authenticated(request)
        if redir is not None:
            return redir

        if _get_rol(request) == "COMPRADOR":
            return view_func(request, *args, **kwargs)

        return redirect("inicio")

    return wrapper


def es_productor(view_func):
    """
    PRODUCTOR:
    - Si no está autenticado => redirect('login')
    - Si el rol no es PRODUCTOR => redirect('inicio')
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        redir = _redirect_login_if_not_authenticated(request)
        if redir is not None:
            return redir

        if _get_rol(request) == "PRODUCTOR":
            return view_func(request, *args, **kwargs)

        return redirect("inicio")

    return wrapper

