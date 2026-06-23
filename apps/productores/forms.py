# apps/productores/forms.py

from django import forms

from .models import Productor


class ProductorForm(forms.ModelForm):

    class Meta:

        model = Productor

        fields = [
            'usuario',
            'nombre_comercial',
            'telefono',
            'direccion',
            'municipio',
            'descripcion',
            'imagen_perfil',
            'latitud',
            'longitud',
            'activo'
        ]

        labels = {
            'usuario': 'Usuario asociado',
            'nombre_comercial': 'Nombre comercial',
            'telefono': 'Telefono',
            'direccion': 'Direccion',
            'municipio': 'Municipio',
            'descripcion': 'Descripcion',
            'imagen_perfil': 'Imagen de perfil',
            'latitud': 'Latitud',
            'longitud': 'Longitud',
            'activo': 'Productor activo',
        }

        widgets = {
            'usuario': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'nombre_comercial': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej: Cafe del Valle'
                }
            ),
            'telefono': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej: 7000-0000'
                }
            ),
            'direccion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Comunidad, zona o referencia'
                }
            ),
            'municipio': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'list': 'municipios-productor',
                    'placeholder': 'Ej: Sacaba'
                }
            ),
            'descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Describe que produce, temporada, forma de entrega o especialidad.'
                }
            ),
            'imagen_perfil': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                    'accept': 'image/*'
                }
            ),
            'latitud': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.000001',
                    'placeholder': '-17.393500'
                }
            ),
            'longitud': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.000001',
                    'placeholder': '-66.157000'
                }
            ),
            'activo': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
        }
