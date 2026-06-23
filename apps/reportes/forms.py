from django import forms

from .models import Incidencia


class IncidenciaForm(forms.ModelForm):
    class Meta:
        model = Incidencia
        fields = ["tipo_incidencia", "descripcion"]
        widgets = {
            "tipo_incidencia": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }
