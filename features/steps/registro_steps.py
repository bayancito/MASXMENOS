from behave import given, when, then
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from apps.usuarios.forms import RegistroForm
from apps.usuarios.models import Perfil


@given("que un visitante completa el formulario de registro")
def completar_registro(context):
    context.client = Client()
    pagina = context.client.get(reverse("registro"))
    context.test.assertEqual(pagina.status_code, 200)
    context.test.assertTemplateUsed(pagina, "usuarios/registro.html")
    context.usuarios_antes = get_user_model().objects.count()
    context.perfiles_antes = Perfil.objects.count()
    context.datos_registro = {
        "username": "nuevo_comprador_bdd",
        "email": "nuevo@example.com",
        "password1": "Bdd-Registro-2026!",
        "password2": "Bdd-Registro-2026!",
        "rol": Perfil.COMPRADOR,
    }
    # Confirm that the remaining data is valid before introducing the mismatch.
    context.test.assertTrue(RegistroForm(context.datos_registro).is_valid())


@given("escribe contraseñas diferentes")
def introducir_contrasenas_diferentes(context):
    context.datos_registro["password2"] = "Bdd-Otra-2026!"


@when("envía el formulario")
def enviar_registro(context):
    context.response = context.client.post(
        reverse("registro"), context.datos_registro
    )


@then("el sistema muestra un error de validación")
def comprobar_error_registro(context):
    context.test.assertEqual(context.response.status_code, 200)
    context.test.assertTemplateUsed(context.response, "usuarios/registro.html")
    formulario = context.response.context["form"]
    context.test.assertIsInstance(formulario, RegistroForm)
    context.test.assertFormError(
        formulario, "password2", "Las contraseñas no coinciden."
    )
    context.test.assertContains(context.response, "Las contraseñas no coinciden.")


@then("no registra un nuevo usuario")
def comprobar_ausencia_usuario(context):
    usuarios = get_user_model().objects
    context.test.assertEqual(usuarios.count(), context.usuarios_antes)
    context.test.assertFalse(
        usuarios.filter(username=context.datos_registro["username"]).exists()
    )
    context.test.assertEqual(Perfil.objects.count(), context.perfiles_antes)
