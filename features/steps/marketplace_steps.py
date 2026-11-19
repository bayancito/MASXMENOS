from decimal import Decimal

from behave import given, when, then
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from apps.productores.models import Productor
from apps.productos.forms import ProductoForm
from apps.productos.models import Categoria, Favorito, Producto
from apps.usuarios.models import Perfil


@given("existen los productos Papa amarilla y Tomate")
def crear_productos_busqueda(context):
    Producto.objects.create(nombre="Papa amarilla", precio=Decimal("8.50"))
    Producto.objects.create(nombre="Tomate", precio=Decimal("6.00"))


@when("busca papa en el catálogo")
def buscar_papa(context):
    context.response = context.client.get(reverse("lista_productos"), {"q": "papa"})


@then("aparece solamente Papa amarilla en los resultados")
def comprobar_busqueda(context):
    context.test.assertEqual(context.response.status_code, 200)
    context.test.assertTemplateUsed(context.response, "productos/lista_productos.html")
    nombres = [producto.nombre for producto in context.response.context["productos"]]
    context.test.assertEqual(nombres, ["Papa amarilla"])
    context.test.assertContains(context.response, "Papa amarilla")
    context.test.assertNotContains(context.response, "Tomate")


@given("el comprador está autenticado")
def autenticar_comprador(context):
    context.client.force_login(context.comprador)


@given("existe un producto para agregar a favoritos")
def crear_producto_favorito(context):
    context.producto = Producto.objects.create(
        nombre="Papa para favoritos", precio=Decimal("8.50")
    )
    context.test.assertFalse(Favorito.objects.filter(usuario=context.comprador).exists())


@when("agrega dos veces el mismo producto a favoritos")
def agregar_favorito_dos_veces(context):
    url = reverse("agregar_favorito", args=[context.producto.pk])
    primera = context.client.get(url)
    context.test.assertRedirects(
        primera, reverse("detalle_producto", args=[context.producto.pk])
    )
    context.test.assertEqual(
        Favorito.objects.filter(
            usuario=context.comprador, producto=context.producto
        ).count(),
        1,
    )
    context.favorito_id = Favorito.objects.get(
        usuario=context.comprador, producto=context.producto
    ).pk
    context.response = context.client.get(url)


@then("se conserva un único favorito del comprador para ese producto")
def comprobar_favorito_unico(context):
    context.test.assertRedirects(
        context.response, reverse("detalle_producto", args=[context.producto.pk])
    )
    favoritos = Favorito.objects.filter(usuario=context.comprador)
    context.test.assertEqual(favoritos.count(), 1)
    favorito = favoritos.get()
    context.test.assertEqual(favorito.producto_id, context.producto.pk)
    context.test.assertEqual(favorito.pk, context.favorito_id)


@when("intenta acceder y enviar datos a la creación de productos")
def intentar_creacion_comprador(context):
    context.productos_antes = Producto.objects.count()
    datos = {"nombre": "Producto no autorizado", "precio": "12.50", "activo": "on"}
    formulario = ProductoForm(datos)
    context.test.assertTrue(formulario.is_valid(), formulario.errors)
    context.respuesta_acceso = context.client.get(reverse("crear_producto"))
    context.response = context.client.post(reverse("crear_producto"), datos)


@then("se le impide crear productos y es redirigido al inicio")
def comprobar_restriccion_comprador(context):
    context.test.assertRedirects(context.respuesta_acceso, reverse("inicio"))
    context.test.assertRedirects(context.response, reverse("inicio"))
    context.test.assertEqual(Producto.objects.count(), context.productos_antes)


@given("un productor autenticado con su perfil comercial")
def preparar_productor(context):
    context.client = Client()
    usuario = get_user_model().objects.create_user(username="productor_marketplace_bdd")
    usuario.perfil.rol = Perfil.PRODUCTOR
    usuario.perfil.save(update_fields=["rol"])
    context.productor = Productor.objects.create(
        usuario=usuario,
        nombre_comercial="Finca BDD",
        telefono="70000000",
        direccion="Comunidad de prueba",
        municipio="Sacaba",
    )
    context.categoria = Categoria.objects.create(nombre="Hortalizas BDD")
    context.client.force_login(usuario)


@when("completa los datos válidos y publica un producto")
def publicar_producto(context):
    pagina = context.client.get(reverse("crear_producto"))
    context.test.assertEqual(pagina.status_code, 200)
    context.test.assertTemplateUsed(pagina, "productos/crear_producto.html")
    context.test.assertIsInstance(pagina.context["form"], ProductoForm)
    context.productos_antes = Producto.objects.count()
    context.datos_producto = {
        "nombre": "Papa publicada BDD",
        "descripcion": "Producto agrícola publicado durante la prueba.",
        "categoria": str(context.categoria.pk),
        "precio": "15.50",
        "activo": "on",
    }
    context.response = context.client.post(
        reverse("crear_producto"), context.datos_producto
    )


@then("el producto queda registrado y asociado al productor correspondiente")
def comprobar_publicacion(context):
    context.test.assertEqual(context.response.status_code, 302)
    context.test.assertEqual(Producto.objects.count(), context.productos_antes + 1)
    producto = Producto.objects.get(nombre=context.datos_producto["nombre"])
    context.test.assertEqual(producto.productor_id, context.productor.pk)
    context.test.assertEqual(producto.categoria_id, context.categoria.pk)
    context.test.assertEqual(producto.precio, Decimal("15.50"))
    context.test.assertEqual(producto.descripcion, context.datos_producto["descripcion"])
    context.test.assertTrue(producto.activo)
    context.test.assertRedirects(
        context.response, reverse("detalle_producto", args=[producto.pk])
    )
