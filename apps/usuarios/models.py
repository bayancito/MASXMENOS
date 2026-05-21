from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):

    ADMIN = "ADMIN"
    PRODUCTOR = "PRODUCTOR"
    COMPRADOR = "COMPRADOR"

    ROLES = [
        (ADMIN, "Administrador"),
        (PRODUCTOR, "Productor"),
        (COMPRADOR, "Comprador"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="perfil"
    )

    rol = models.CharField(
        max_length=20,
        choices=ROLES,
        default=COMPRADOR
    )

    telefono = models.CharField(
        max_length=20,
        blank=True
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.rol}"