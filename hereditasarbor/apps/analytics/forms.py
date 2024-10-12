from django import forms
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from .models import Analytic


class AnalyticCreateForm(forms.ModelForm):
    class Meta:
        model = Analytic
        fields = ("user", "", "")
