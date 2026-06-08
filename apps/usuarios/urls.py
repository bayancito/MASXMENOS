from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import inicio, registro, perfil_usuario

urlpatterns = [
    path("", inicio, name="inicio"),
    path(
        "login/",
        LoginView.as_view(
            template_name="registration/login.html"
        ),
        name="login"
    ),

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout"
    ),

    path(
        "registro/",
        registro,
        name="registro"
    ),

    path(
        "perfil/",
        perfil_usuario,
        name="perfil"
    ),
]
