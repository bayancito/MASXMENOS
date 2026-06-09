from django.shortcuts import redirect


def es_admin(view_func):
    def wrapper(request, *args, **kwargs):
        if (
            request.user.is_authenticated
            and getattr(request.user, "perfil", None) is not None
            and request.user.perfil.rol == "ADMIN"
        ):
            return view_func(request, *args, **kwargs)

        return redirect("inicio")

    return wrapper


def es_productor_o_admin(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        perfil = getattr(request.user, "perfil", None)
        rol = getattr(perfil, "rol", None)

        if rol in ["ADMIN", "PRODUCTOR"]:
            return view_func(request, *args, **kwargs)

        return redirect("inicio")

    return wrapper

