from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.productores.models import Productor
from apps.productos.models import Producto
from apps.usuarios.models import Perfil


class AutorizacionEdicionProductoTests(TestCase):
    def setUp(self):
        self.propietario = get_user_model().objects.create_user(username="propietario")
        self.propietario.perfil.rol = Perfil.PRODUCTOR
        self.propietario.perfil.save(update_fields=["rol"])
        self.productor = Productor.objects.create(
            usuario=self.propietario,
            nombre_comercial="Finca de prueba",
            telefono="70000000",
            direccion="Comunidad de prueba",
            municipio="Sacaba",
        )
        self.producto = Producto.objects.create(
            nombre="Nombre original", productor=self.productor, precio="10.00"
        )
        self.url = reverse("editar_producto", args=[self.producto.pk])
        self.datos = {"nombre": "Nombre editado", "precio": "12.50", "activo": "on"}

    def test_anonimo_no_puede_modificar_producto(self):
        respuesta = self.client.post(self.url, self.datos)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, "Nombre original")
        self.assertRedirects(respuesta, reverse("login"))

    def test_comprador_no_puede_modificar_aunque_este_asociado_al_productor(self):
        self.propietario.perfil.rol = Perfil.COMPRADOR
        self.propietario.perfil.save(update_fields=["rol"])
        self.client.force_login(self.propietario)
        respuesta = self.client.post(self.url, self.datos)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, "Nombre original")
        self.assertRedirects(respuesta, reverse("inicio"))

    def test_usuario_sin_perfil_no_puede_modificar(self):
        usuario = get_user_model().objects.create_user(username="sin_perfil")
        usuario.perfil.delete()
        self.client.force_login(usuario)
        respuesta = self.client.post(self.url, self.datos)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, "Nombre original")
        self.assertRedirects(respuesta, reverse("inicio"))

    def test_productor_ajeno_no_puede_modificar(self):
        usuario = get_user_model().objects.create_user(username="otro_productor")
        usuario.perfil.rol = Perfil.PRODUCTOR
        usuario.perfil.save(update_fields=["rol"])
        self.client.force_login(usuario)
        respuesta = self.client.post(self.url, self.datos)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, "Nombre original")
        self.assertRedirects(respuesta, reverse("lista_productos"))

    def test_productor_no_puede_modificar_producto_sin_propietario(self):
        self.producto.productor = None
        self.producto.save(update_fields=["productor"])
        self.client.force_login(self.propietario)
        respuesta = self.client.post(self.url, self.datos)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, "Nombre original")
        self.assertRedirects(respuesta, reverse("lista_productos"))

    def test_propietario_puede_ver_formulario_y_modificar(self):
        self.client.force_login(self.propietario)
        pagina = self.client.get(self.url)
        self.assertEqual(pagina.status_code, 200)
        self.assertTemplateUsed(pagina, "productos/editar_producto.html")
        respuesta = self.client.post(self.url, self.datos)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, "Nombre editado")
        self.assertEqual(self.producto.productor_id, self.productor.pk)
        self.assertRedirects(
            respuesta, reverse("detalle_producto", args=[self.producto.pk])
        )

    def test_administrador_conserva_permiso_de_edicion(self):
        usuario = get_user_model().objects.create_user(username="administrador")
        usuario.perfil.rol = Perfil.ADMIN
        usuario.perfil.save(update_fields=["rol"])
        self.client.force_login(usuario)
        respuesta = self.client.post(self.url, self.datos)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, "Nombre editado")
        self.assertRedirects(
            respuesta, reverse("detalle_producto", args=[self.producto.pk])
        )
