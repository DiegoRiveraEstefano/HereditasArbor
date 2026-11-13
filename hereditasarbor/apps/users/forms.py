from django import forms
from django.forms import widgets

from .models import User


class UserCreationForm(forms.ModelForm):
    """user creation form, used for creating new users.
    Inherits from django.forms.ModelForm.

    Fields:
        username: username field
        email: email field
        password: password field
        name: name field
    """

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
    """user login form, used for logging in users.
    Inherits from django.forms.Form.

    Fields:
        username: username field
        password: password field
    """

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
    """user logout form, used for logging out users.
    Inherits from django.forms.Form.

    Fields:
        confirmation: confirmation field
    """

    confirmation = forms.BooleanField(
        required=True,
        label="Usuario",
        widget=widgets.HiddenInput,
        initial=True,
    )
