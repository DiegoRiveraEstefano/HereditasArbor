from django import forms
from django.utils.translation import gettext_lazy as _

from hereditasarbor.apps.mixins.fields import TailwindDateField

from .models import Familiar
from .models import FamilyTree


class FamiliarForm(forms.ModelForm):
    tree = forms.ChoiceField(choices=[], required=True, widget=forms.HiddenInput)

    birth_date = TailwindDateField(
        label="Fecha Nacimiento",
        required=False,
    )

    death_date = forms.DateField(
        label="Fecha Muerte(solo si aplica)",
        required=False,
        widget=forms.widgets.DateTimeInput,
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", "")
        super().__init__(*args, **kwargs)
        self.fields["tree"] = forms.ModelChoiceField(
            queryset=FamilyTree.objects.filter(owner=user),
            widget=forms.HiddenInput,
        )

    class Meta:
        model = Familiar
        fields = (
            "name",
            "sex",
            "relation_type",
            "birth_date",
            "weight",
            "height",
            "death_date",
            "tree",
        )


class FamiliarUpdateForm(forms.ModelForm):
    birth_date = forms.fields.DateField(
        label="Fecha Nacimiento", required=False, widget=forms.widgets.DateInput
    )

    death_date = forms.DateField(
        label="Fecha Muerte(solo si aplica)",
        required=False,
        widget=forms.widgets.DateTimeInput,
    )

    class Meta:
        model = Familiar
        fields = (
            "name",
            "sex",
            "relation_type",
            "birth_date",
            "weight",
            "height",
            "death_date",
        )
