from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.productores.models import Productor
from apps.usuarios.models import Perfil

from .models import Categoria, Producto, Solicitud, ContactoProducto, SolicitudCompra


class ContactarProductorWhatsappTests(TestCase):
    def setUp(self):
        self.comprador = User.objects.create_user(
            username='comprador',
            password='testpass123'
        )
        self.comprador.perfil.rol = Perfil.COMPRADOR
        self.comprador.perfil.save()

        self.productor_user = User.objects.create_user(
            username='productor',
            password='testpass123'
        )
        self.productor_user.perfil.rol = Perfil.PRODUCTOR
        self.productor_user.perfil.save()

        self.productor = Productor.objects.create(
            usuario=self.productor_user,
            nombre_comercial='Finca Central',
            telefono='+591 7070-1234',
            direccion='Camino rural',
            municipio='Cochabamba',
        )
        self.categoria = Categoria.objects.create(nombre='Hortalizas')
        self.producto = Producto.objects.create(
            nombre='Papa holandesa',
            categoria=self.categoria,
            productor=self.productor,
            activo=True,
        )

    def test_registra_contacto_y_redirige_a_whatsapp(self):
        self.client.login(username='comprador', password='testpass123')

        response = self.client.get(
            reverse('contactar_productor_whatsapp', args=[self.producto.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].startswith('https://wa.me/59170701234?text='))

        self.assertEqual(Solicitud.objects.count(), 0)

        contacto = ContactoProducto.objects.get()
        self.assertEqual(contacto.comprador, self.comprador)
        self.assertEqual(contacto.productor, self.productor)
        self.assertEqual(contacto.producto, self.producto)
        self.assertEqual(contacto.canal, ContactoProducto.CANAL_WHATSAPP)
        self.assertIn('Papa holandesa', contacto.mensaje)

    def test_solicitud_compra_guarda_datos_y_redirige_a_whatsapp(self):
        self.client.login(username='comprador', password='testpass123')

        response = self.client.post(
            reverse('solicitar_producto', args=[self.producto.pk]),
            {
                'cantidad_solicitada': 7,
                'mensaje_adicional': 'Necesito entrega para el viernes.',
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].startswith('https://wa.me/59170701234?text='))
        self.assertIn('Papa%20holandesa', response['Location'])
        self.assertIn('Cantidad%20solicitada%3A%207', response['Location'])
        self.assertIn('Necesito%20entrega%20para%20el%20viernes', response['Location'])

        solicitud = SolicitudCompra.objects.get()
        self.assertEqual(solicitud.comprador, self.comprador)
        self.assertEqual(solicitud.productor, self.productor)
        self.assertEqual(solicitud.producto, self.producto)
        self.assertEqual(solicitud.cantidad_solicitada, 7)
        self.assertEqual(solicitud.mensaje_adicional, 'Necesito entrega para el viernes.')
        self.assertEqual(solicitud.estado, SolicitudCompra.PENDIENTE)
