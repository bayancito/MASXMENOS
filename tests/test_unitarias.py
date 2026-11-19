from types import SimpleNamespace

from django.test import SimpleTestCase

from apps.productos.views import (
    _mensaje_whatsapp_solicitud_compra,
    _normalizar_telefono_whatsapp,
)
from apps.usuarios.forms import RegistroForm
from apps.usuarios.models import Perfil


class NormalizarTelefonoTests(SimpleTestCase):
    def test_elimina_caracteres_no_numericos(self):
        self.assertEqual(
            _normalizar_telefono_whatsapp("+591 (7070)-1234"), "59170701234"
        )

    def test_elimina_prefijo_internacional_00(self):
        self.assertEqual(
            _normalizar_telefono_whatsapp("00591 7070 1234"), "59170701234"
        )

    def test_entradas_sin_numero_devuelven_cadena_vacia(self):
        for telefono in (None, "", "  ", "sin teléfono"):
            with self.subTest(telefono=telefono):
                self.assertEqual(_normalizar_telefono_whatsapp(telefono), "")


class RegistroFormTests(SimpleTestCase):
    def setUp(self):
        self.datos = {
            "username": "comprador_unitario",
            "email": "comprador@example.com",
            "password1": "Registro-Unitario-2026!",
            "password2": "Registro-Unitario-2026!",
            "rol": Perfil.COMPRADOR,
        }

    def test_acepta_contrasenas_coincidentes(self):
        formulario = RegistroForm(self.datos)
        self.assertTrue(formulario.is_valid(), formulario.errors)
        self.assertEqual(formulario.cleaned_data["rol"], Perfil.COMPRADOR)

    def test_rechaza_contrasenas_diferentes(self):
        self.datos["password2"] = "Otra-Unitario-2026!"
        formulario = RegistroForm(self.datos)
        self.assertFalse(formulario.is_valid())
        self.assertEqual(set(formulario.errors), {"password2"})
        self.assertFormError(
            formulario, "password2", "Las contraseñas no coinciden."
        )


class MensajeSolicitudTests(SimpleTestCase):
    def test_incluye_mensaje_adicional(self):
        solicitud = SimpleNamespace(
            producto=SimpleNamespace(nombre="Papa amarilla"),
            cantidad_solicitada=7,
            mensaje_adicional="Entrega mañana.",
        )
        self.assertEqual(
            _mensaje_whatsapp_solicitud_compra(solicitud),
            "Hola, estoy interesado en el producto Papa amarilla. "
            "Cantidad solicitada: 7. Mensaje adicional: Entrega mañana.",
        )

    def test_omite_mensaje_adicional_vacio(self):
        solicitud = SimpleNamespace(
            producto=SimpleNamespace(nombre="Tomate"),
            cantidad_solicitada=3,
            mensaje_adicional="",
        )
        self.assertEqual(
            _mensaje_whatsapp_solicitud_compra(solicitud),
            "Hola, estoy interesado en el producto Tomate. Cantidad solicitada: 3.",
        )
