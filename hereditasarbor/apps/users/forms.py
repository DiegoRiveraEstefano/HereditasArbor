from django import forms
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from .models import User


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(
        max_length=128,
        required=True,
        label="Contraseña",
        widget=widgets.PasswordInput,
    )

    email = forms.CharField(
        max_length=128,
        required=True,
        label="Correo",
        widget=widgets.EmailInput,
    )

    class Meta:
        model = User
        fields = ("username", "email", "name", "password")


class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=128,
        required=True,
        label="Usuario",
        widget=widgets.TextInput,
    )

    password = forms.CharField(
        max_length=128,
        required=True,
        label="Contraseña",
        widget=widgets.PasswordInput,
    )


class UserLogOutForm(forms.Form):
    confirmation = forms.BooleanField(
        required=True,
        label="Usuario",
        widget=widgets.HiddenInput,
        initial=True,
    )
