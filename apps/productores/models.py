from django.db import models
from django.contrib.auth.models import User

class Productor(models.Model):

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='productor'
    )

    nombre_comercial = models.CharField(
        max_length=150
    )

    telefono = models.CharField(
        max_length=30
    )

    direccion = models.CharField(
        max_length=255
    )

    municipio = models.CharField(
        max_length=100
    )

    latitud = models.DecimalField(
    max_digits=9,
    decimal_places=6,
    null=True,
    blank=True
)

    longitud = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )

    activo = models.BooleanField(
        default=True
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Productor"
        verbose_name_plural = "Productores"
        ordering = ['nombre_comercial']

    def __str__(self):
        return self.nombre_comercial