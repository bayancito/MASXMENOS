from django.db import models
from apps.productores.models import Productor
from django.contrib.auth.models import User
from decimal import Decimal


class Categoria(models.Model):

    nombre = models.CharField(
        max_length=100,
        unique=True
    )

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    activa = models.BooleanField(
        default=True
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Producto(models.Model):

    nombre = models.CharField(
        max_length=150
    )

    descripcion = models.TextField(
        blank=True,
        null=True
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos',
        null=True,
        blank=True
    )

    productor = models.ForeignKey(
        Productor,
        on_delete=models.CASCADE,
        related_name='productos',
        null=True,
        blank=True
    )

    imagen = models.ImageField(
        upload_to='productos/',
        blank=True,
        null=True
    )

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Precio en Bs. (moneda local)"
    )

    activo = models.BooleanField(
        default=True
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class ProductoImagen(models.Model):

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='imagenes'
    )

    imagen = models.ImageField(
        upload_to='productos/galeria/'
    )

    texto_alternativo = models.CharField(
        max_length=150,
        blank=True
    )

    orden = models.PositiveIntegerField(
        default=0
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Imagen de producto"
        verbose_name_plural = "Imagenes de producto"
        ordering = ['orden', 'id']

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"


class Solicitud(models.Model):

    comprador = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='solicitudes',
    )

    producto = models.ForeignKey(
        'Producto',
        on_delete=models.CASCADE,
        related_name='solicitudes',
    )

    productor = models.ForeignKey(
        Productor,
        on_delete=models.SET_NULL,
        related_name='solicitudes_recibidas',
        null=True,
        blank=True,
    )

    cantidad = models.PositiveIntegerField()
    mensaje = models.TextField(blank=True)

    PENDIENTE = "PENDIENTE"
    ACEPTADA = "ACEPTADA"
    RECHAZADA = "RECHAZADA"

    ESTADOS = [
        (PENDIENTE, "Pendiente"),
        (ACEPTADA, "Aceptada"),
        (RECHAZADA, "Rechazada"),
    ]

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default=PENDIENTE,
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solicitud({self.id}) — {self.comprador.username} — {self.producto.nombre}"


class ContactoProducto(models.Model):

    CANAL_WHATSAPP = "WHATSAPP"

    CANALES = [
        (CANAL_WHATSAPP, "WhatsApp"),
    ]

    comprador = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='contactos_producto',
    )

    productor = models.ForeignKey(
        Productor,
        on_delete=models.SET_NULL,
        related_name='contactos_recibidos',
        null=True,
        blank=True,
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='contactos',
    )

    canal = models.CharField(
        max_length=20,
        choices=CANALES,
        default=CANAL_WHATSAPP,
    )

    mensaje = models.TextField(blank=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contacto de producto"
        verbose_name_plural = "Contactos de producto"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Contacto({self.id}) - {self.comprador.username} - {self.producto.nombre}"


class SolicitudCompra(models.Model):

    comprador = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='solicitudes_compra',
    )

    productor = models.ForeignKey(
        Productor,
        on_delete=models.SET_NULL,
        related_name='solicitudes_compra_recibidas',
        null=True,
        blank=True,
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='solicitudes_compra',
    )

    cantidad_solicitada = models.PositiveIntegerField()
    mensaje_adicional = models.TextField(blank=True)

    PENDIENTE = "PENDIENTE"
    ACEPTADA = "ACEPTADA"
    RECHAZADA = "RECHAZADA"

    ESTADOS = [
        (PENDIENTE, "Pendiente"),
        (ACEPTADA, "Aceptada"),
        (RECHAZADA, "Rechazada"),
    ]

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default=PENDIENTE,
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Solicitud de compra"
        verbose_name_plural = "Solicitudes de compra"
        ordering = ['-fecha_creacion']

    @property
    def cantidad(self):
        return self.cantidad_solicitada

    @property
    def mensaje(self):
        return self.mensaje_adicional

    def __str__(self):
        return f"SolicitudCompra({self.id}) - {self.comprador.username} - {self.producto.nombre}"


class Cosecha(models.Model):
    UNIDAD_ARROBAS = "ARROBAS"
    UNIDAD_LIBRAS = "LIBRAS"
    UNIDAD_QUINTALES = "QUINTALES"

    UNIDADES = [
        (UNIDAD_ARROBAS, "arrobas"),
        (UNIDAD_LIBRAS, "libras"),
        (UNIDAD_QUINTALES, "quintales"),
    ]

    DISPONIBLE = "DISPONIBLE"
    RESERVADA = "RESERVADA"
    VENDIDA = "VENDIDA"

    ESTADOS = [
        (DISPONIBLE, "disponible"),
        (RESERVADA, "reservada"),
        (VENDIDA, "vendida"),
    ]

    productor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cosechas",
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="cosechas",
    )

    cantidad = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    unidad_medida = models.CharField(
        max_length=20,
        choices=UNIDADES,
    )

    precio_esperado = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Precio esperado en Bs. (moneda local)"
    )

    fecha_cosecha = models.DateField()

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default=DISPONIBLE,
    )

    fotografia = models.ImageField(
        upload_to="cosechas/",
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Cosecha"
        verbose_name_plural = "Cosechas"
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"Cosecha({self.id}) — {self.producto.nombre} — {self.cantidad} {self.unidad_medida}"


class Favorito(models.Model):


    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favoritos'
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='favoritos'
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("usuario", "producto")
        verbose_name = "Favorito"
        verbose_name_plural = "Favoritos"

    def __str__(self):
        return f"{self.usuario.username} - {self.producto.nombre}"
