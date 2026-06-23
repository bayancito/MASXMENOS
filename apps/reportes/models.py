from django.conf import settings
from django.db import models


class Incidencia(models.Model):
    TIPO_BLOQUEO = "bloqueo"
    TIPO_INUNDACION = "inundacion"
    TIPO_SEQUIA = "sequia"
    TIPO_DERRUMBE = "derrumbe"
    TIPO_OTRO = "otro"

    TIPO_INCIDENCIA_CHOICES = [
        (TIPO_BLOQUEO, "Bloqueo"),
        (TIPO_INUNDACION, "Inundación"),
        (TIPO_SEQUIA, "Sequía"),
        (TIPO_DERRUMBE, "Derrumbe"),
        (TIPO_OTRO, "Otro"),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="incidencias",
    )
    tipo_incidencia = models.CharField(
        max_length=20,
        choices=TIPO_INCIDENCIA_CHOICES,
    )
    descripcion = models.TextField()
    fecha_reporte = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"Incidencia({self.tipo_incidencia}) - {self.usuario} - {self.fecha_reporte}"
