from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Familiar
from .models import FamiliarDiseases


class FamiliarForm(forms.ModelForm):

    class Meta:
        model = Familiar
        fields = ("name", "sex", "relation_type", "birth_date", "weight", "height")


class FamiliarDiseasesForm(forms.ModelForm):
    class Meta:
        model = FamiliarDiseases
        fields = ("familiar", "disease")
