from behave import given, when, then
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from apps.usuarios.models import Perfil


@given("que existe un comprador registrado con credenciales válidas")
def crear_comprador(context):
    context.client = Client()
    context.login_password = "Bdd-Comprador-2026!"
    context.comprador = get_user_model().objects.create_user(
        username="comprador_bdd",
        email="comprador@example.com",
        password=context.login_password,
    )
    context.comprador.perfil.rol = Perfil.COMPRADOR
    context.comprador.perfil.save(update_fields=["rol"])


@when("introduce sus credenciales en el formulario de login")
def enviar_login(context):
    pagina = context.client.get(reverse("login"))
    context.test.assertEqual(pagina.status_code, 200)
    context.test.assertTemplateUsed(pagina, "registration/login.html")
    context.response = context.client.post(
        reverse("login"),
        {
            "username": context.comprador.username,
            "password": context.login_password,
        },
    )


@then("el sistema lo autentica y redirige al inicio")
def comprobar_login(context):
    context.test.assertRedirects(context.response, reverse("inicio"))
    context.test.assertEqual(
        context.client.session["_auth_user_id"], str(context.comprador.pk)
    )
    inicio = context.client.get(reverse("inicio"))
    context.test.assertTrue(inicio.wsgi_request.user.is_authenticated)
    context.test.assertEqual(inicio.wsgi_request.user.pk, context.comprador.pk)
