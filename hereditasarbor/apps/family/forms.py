from django import forms

from .models import Familiar
from .models import FamilyTree


class FamiliarForm(forms.ModelForm):
    """FamiliarForm, used to create a new familiar.

    Args:
        user (User): user model
        tree (FamilyTree): family tree model
    Fields:
        name: name field
        sex: sex field
        relation_type: relation type field
        birth_date: birth date field
        weight: weight field
        height: height field
        death_date: death date field
        tree: tree field
    """

    tree = forms.ChoiceField(choices=[], required=True, widget=forms.HiddenInput)

    birth_date = forms.DateField(
        label="Fecha Nacimiento",
        required=True,
        widget=forms.widgets.DateTimeInput,
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
    """FamiliarUpdateForm, used to update a familiar.

    Args:
        user (User): user model
    Fields:
        name: name field
        sex: sex field
        relation_type: relation type field
        birth_date: birth date field
        weight: weight field
        height: height field
        death_date: death date field
    """

    birth_date = forms.DateField(
        label="Fecha Nacimiento",
        required=True,
        widget=forms.widgets.DateTimeInput,
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
