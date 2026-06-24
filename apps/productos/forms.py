from django import forms

from .models import Producto, Solicitud, Cosecha, SolicitudCompra


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        files = data if isinstance(data, (list, tuple)) else [data]
        return [
            super(MultipleImageField, self).clean(file, initial)
            for file in files
            if file
        ]


class ProductoForm(forms.ModelForm):
    imagenes = MultipleImageField(
        label="Fotos adicionales",
        required=False,
        help_text="Puedes seleccionar varias fotos para la galeria del producto.",
        widget=MultipleFileInput(
            attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'multiple': True,
            }
        )
    )

    class Meta:
        model = Producto

        fields = [
            'nombre',
            'descripcion',
            'categoria',
            'precio',
            'imagen',
            'imagenes',
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
                attrs={'class': 'form-control', 'accept': 'image/*'}
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


class SolicitudCompraForm(forms.ModelForm):

    class Meta:
        model = SolicitudCompra
        fields = [
            'cantidad_solicitada',
            'mensaje_adicional',
        ]

        labels = {
            'cantidad_solicitada': 'Cantidad solicitada',
            'mensaje_adicional': 'Mensaje adicional',
        }

        widgets = {
            'cantidad_solicitada': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 1,
                    'placeholder': 'Ej. 5',
                }
            ),
            'mensaje_adicional': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Ej. Quisiera coordinar entrega para mañana.',
                }
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

