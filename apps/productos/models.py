from django.db import models
from apps.productores.models import Productor
from django.contrib.auth.models import User


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
