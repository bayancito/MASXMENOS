from django import forms

from .models import Producto, Solicitud, Cosecha


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


class CosechaForm(forms.ModelForm):

    class Meta:
        model = Cosecha
        fields = [
            'producto',
            'cantidad',
            'unidad_medida',
            'precio_esperado',
            'fecha_cosecha',
            'estado',
            'fotografia',
        ]

        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'unidad_medida': forms.Select(attrs={'class': 'form-select'}),
            'precio_esperado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'fecha_cosecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'fotografia': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

