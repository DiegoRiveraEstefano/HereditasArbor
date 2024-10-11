from django import forms
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from hereditasarbor.apps.users.models import User

from .models import PersonalData
from .models import PersonalTimeStampData


class PersonalDataCreateForm(forms.ModelForm):
    user = forms.ChoiceField(choices=[], required=True, widget=forms.HiddenInput)

    class Meta:
        model = PersonalData
        fields = ("user", "first_name", "last_name", "birth_day", "sex")

    def __init__(self, *args, **kwargs):
        user: User = kwargs.pop("user", "")
        super().__init__(*args, **kwargs)
        self.fields["user"] = forms.ModelChoiceField(
            queryset=User.objects.filter(username=user.username),
            widget=forms.HiddenInput,
        )


class PersonalDataUpdateForm(forms.ModelForm):
    class Meta:
        model = PersonalData
        fields = ("first_name", "last_name", "birth_day", "sex")


class PersonalTimeStampDataCreateForm(forms.ModelForm):
    personal_data = forms.ChoiceField(
        choices=[], required=True, widget=forms.HiddenInput
    )

    class Meta:
        model = PersonalTimeStampData
        fields = (
            "personal_data",
            "weight",
            "height",
            "cardiac_pulse",
            "glucose",
            "cholesterol",
        )

    def __init__(self, *args, **kwargs):
        user: User = kwargs.pop("user", "")
        super().__init__(*args, **kwargs)
        self.fields["personal_data"] = forms.ModelChoiceField(
            queryset=PersonalData.objects.filter(user=user),
            widget=forms.HiddenInput,
        )


class PersonalTimeStampDataUpdateForm(forms.ModelForm):
    class Meta:
        model = PersonalTimeStampData
        fields = (
            "weight",
            "height",
            "cardiac_pulse",
            "glucose",
            "cholesterol",
        )
