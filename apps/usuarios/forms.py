from django import forms
from django.contrib.auth.models import User

from .models import Perfil


class RegistroForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="Usuario",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    rol = forms.ChoiceField(
        label="Rol",
        choices=[
            (Perfil.PRODUCTOR, "Productor"),
            (Perfil.COMPRADOR, "Comprador"),
        ],
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    telefono = forms.CharField(
        label="Teléfono",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    zona = forms.CharField(
        label="Zona",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Las contraseñas no coinciden.")

        return cleaned_data

    def save(self):
        username = self.cleaned_data["username"]
        email = self.cleaned_data["email"]
        password1 = self.cleaned_data["password1"]

        rol = self.cleaned_data["rol"]
        telefono = self.cleaned_data.get("telefono", "")
        zona = self.cleaned_data.get("zona", "")

        user = User.objects.create(
            username=username,
            email=email,
        )
        user.set_password(password1)
        user.save()

        # Perfil se crea automáticamente por signals.py, pero lo cubrimos por seguridad.
        perfil, _ = Perfil.objects.get_or_create(user=user)

        perfil.rol = rol
        perfil.telefono = telefono
        perfil.zona = zona
        perfil.save()

        return user


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ("telefono", "zona", "foto_perfil")
        widgets = {
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "zona": forms.TextInput(attrs={"class": "form-control"}),
        }
