from urllib.parse import parse_qs, urlsplit

from behave import given, when, then
from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.productores.models import Productor
from apps.productos.models import Producto, SolicitudCompra
from apps.usuarios.models import Perfil


@given("existe un producto activo de un productor con WhatsApp")
def preparar_producto_solicitable(context):
    usuario = get_user_model().objects.create_user(username="vendedor_solicitud_bdd")
    usuario.perfil.rol = Perfil.PRODUCTOR
    usuario.perfil.save(update_fields=["rol"])
    context.productor = Productor.objects.create(
        usuario=usuario,
        nombre_comercial="Finca de solicitudes BDD",
        telefono="+591 7000-0000",
        direccion="Comunidad de prueba",
        municipio="Sacaba",
    )
    context.producto = Producto.objects.create(
        nombre="Papa amarilla para solicitud",
        productor=context.productor,
        precio="12.50",
        activo=True,
    )


@when("solicita el producto con cantidad y mensaje válidos")
def enviar_solicitud(context):
    context.solicitudes_antes = SolicitudCompra.objects.count()
    context.datos_solicitud = {
        "cantidad_solicitada": 7,
        "mensaje_adicional": "Coordinar entrega para mañana.",
    }
    context.response = context.client.post(
        reverse("solicitar_producto", args=[context.producto.pk]),
        context.datos_solicitud,
        follow=False,
    )


@then("se registra una solicitud de compra pendiente")
def comprobar_solicitud_pendiente(context):
    context.test.assertEqual(context.response.status_code, 302)
    context.test.assertEqual(
        SolicitudCompra.objects.count(), context.solicitudes_antes + 1
    )
    context.solicitud = SolicitudCompra.objects.get(
        comprador=context.comprador, producto=context.producto
    )
    context.test.assertEqual(context.solicitud.productor_id, context.productor.pk)
    context.test.assertEqual(context.solicitud.estado, SolicitudCompra.PENDIENTE)
    context.test.assertEqual(
        context.solicitud.cantidad_solicitada,
        context.datos_solicitud["cantidad_solicitada"],
    )
    context.test.assertEqual(
        context.solicitud.mensaje_adicional,
        context.datos_solicitud["mensaje_adicional"],
    )


@then("la respuesta redirige a WhatsApp con los datos de la solicitud")
def comprobar_redireccion_whatsapp(context):
    context.test.assertEqual(context.response.status_code, 302)
    destino = urlsplit(context.response["Location"])
    context.test.assertEqual(destino.scheme, "https")
    context.test.assertEqual(destino.netloc, "wa.me")
    context.test.assertEqual(destino.path, "/59170000000")
    context.test.assertEqual(destino.fragment, "")
    mensaje = (
        f"Hola, estoy interesado en el producto {context.producto.nombre}. "
        "Cantidad solicitada: 7. "
        "Mensaje adicional: Coordinar entrega para mañana."
    )
    context.test.assertEqual(parse_qs(destino.query), {"text": [mensaje]})


@given("tiene una solicitud de compra pendiente")
def preparar_solicitud_pendiente(context):
    comprador = get_user_model().objects.create_user(username="solicitante_bdd")
    context.test.assertEqual(comprador.perfil.rol, Perfil.COMPRADOR)
    producto = Producto.objects.create(
        nombre="Producto solicitado BDD", productor=context.productor, activo=True
    )
    context.solicitud = SolicitudCompra.objects.create(
        comprador=comprador,
        productor=context.productor,
        producto=producto,
        cantidad_solicitada=3,
        mensaje_adicional="Entrega coordinada.",
        estado=SolicitudCompra.PENDIENTE,
    )
    context.estado_original = context.solicitud.estado


@given("se autentica un productor diferente al propietario de la solicitud")
def autenticar_productor_ajeno(context):
    usuario = get_user_model().objects.create_user(username="productor_ajeno_bdd")
    usuario.perfil.rol = Perfil.PRODUCTOR
    usuario.perfil.save(update_fields=["rol"])
    productor_ajeno = Productor.objects.create(
        usuario=usuario,
        nombre_comercial="Otra finca BDD",
        telefono="70000001",
        direccion="Otra comunidad",
        municipio="Sacaba",
    )
    context.test.assertNotEqual(productor_ajeno.pk, context.solicitud.productor_id)
    context.client.force_login(usuario)


@when("acepta la solicitud mediante POST")
def aceptar_solicitud_por_post(context):
    context.response = context.client.post(
        reverse("aceptar_solicitud", args=[context.solicitud.pk]), follow=False
    )


@then("la solicitud queda aceptada")
def comprobar_solicitud_aceptada(context):
    context.solicitud.refresh_from_db()
    context.test.assertEqual(context.solicitud.estado, SolicitudCompra.ACEPTADA)
    context.test.assertRedirects(context.response, reverse("solicitudes_recibidas"))


@then("se deniega la operación y la solicitud conserva su estado original")
def comprobar_denegacion_solicitud(context):
    context.test.assertRedirects(context.response, reverse("inicio"))
    context.solicitud.refresh_from_db()
    context.test.assertEqual(context.estado_original, SolicitudCompra.PENDIENTE)
    context.test.assertEqual(context.solicitud.estado, context.estado_original)
    context.test.assertEqual(context.solicitud.productor_id, context.productor.pk)
