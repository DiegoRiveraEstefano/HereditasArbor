from django import forms
from django.utils.translation import gettext_lazy as _

from hereditasarbor.apps.family.models import Familiar

from .models import FamiliarDiseases


class FamiliarDiseasesForm(forms.ModelForm):
    class Meta:
        model = FamiliarDiseases
        fields = ("familiar", "disease")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", "")
        super().__init__(*args, **kwargs)
        self.fields["familiar"] = forms.ModelChoiceField(
            queryset=Familiar.objects.filter(tree__owner=user),
            widget=forms.widgets.HiddenInput,
        )
