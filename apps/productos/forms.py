from django import forms

from .models import Producto, Solicitud


class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto

        fields = [
            'nombre',
            'descripcion',
            'categoria',
            'precio',
            'imagen',
            'activo'
        ]

        widgets = {
            'nombre': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'descripcion': forms.Textarea(
                attrs={'class': 'form-control'}
            ),

            'categoria': forms.Select(
                attrs={'class': 'form-select'}
            ),

            'precio': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}
            ),

            'imagen': forms.ClearableFileInput(
                attrs={'class': 'form-control'}
            ),

        }


class SolicitudForm(forms.ModelForm):

    class Meta:
        model = Solicitud
        fields = [
            'cantidad',
            'mensaje',
        ]

        widgets = {
            'cantidad': forms.NumberInput(
                attrs={'class': 'form-control', 'min': 1}
            ),
            'mensaje': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4}
            ),
        }

