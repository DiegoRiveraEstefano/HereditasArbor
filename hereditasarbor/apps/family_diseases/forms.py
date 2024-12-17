from django import forms
from django.utils.translation import gettext_lazy as _

from hereditasarbor.apps.family.models import Familiar

from .models import FamiliarDiseases


class FamiliarDiseasesForm(forms.ModelForm):
    """FamiliarDiseasesForm, used to create a new familiar diseases.

    Args:
        user (User): user model
        familiar (Familiar): familiar model
        disease (Disease): disease model
    Fields:
        familiar: familiar model
        disease: disease model
    """

    class Meta:
        model = FamiliarDiseases
        fields = ("familiar", "disease")

    def __init__(self, *args, **kwargs):
        """Initialize the form.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        user = kwargs.pop("user", "")
        super().__init__(*args, **kwargs)
        self.fields["familiar"] = forms.ModelChoiceField(
            queryset=Familiar.objects.filter(tree__owner=user),
            widget=forms.widgets.HiddenInput,
        )
