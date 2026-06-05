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
            'latitud',
            'longitud',
            'activo'
        ]