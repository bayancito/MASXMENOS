from behave import given, when, then
from django.test import Client
from django.urls import reverse


@given("un visitante sin iniciar sesión")
def visitante_sin_sesion(context):
    context.client = Client()


@when("intenta acceder a sus favoritos")
def acceder_a_favoritos(context):
    context.response = context.client.get(reverse("mis_favoritos"))


@then("es redirigido al login")
def comprobar_redireccion(context):
    assert context.response.status_code == 302, context.response.status_code
    assert context.response["Location"] == reverse("login"), context.response["Location"]
    assert "_auth_user_id" not in context.client.session
