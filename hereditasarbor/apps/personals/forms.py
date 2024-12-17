from django import forms
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from hereditasarbor.apps.users.models import User

from .models import PersonalData
from .models import PersonalTimeStampData


class PersonalDataCreateForm(forms.ModelForm):

    """PersonalDataCreateForm, used to create a new personal data.

    Args:
        user (User): user model
    Fields:
        user: user model
        first_name: first name field
        last_name: last name field
        birth_day: birth day field
        sex: sex field
    """

    user = forms.ChoiceField(choices=[], required=True, widget=forms.HiddenInput)

    class Meta:
        model = PersonalData
        fields = ("user", "first_name", "last_name", "birth_day", "sex")

    def __init__(self, *args, **kwargs):
        """Initialize the form.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """

        user: User = kwargs.pop("user", "")
        super().__init__(*args, **kwargs)
        self.fields["user"] = forms.ModelChoiceField(
            queryset=User.objects.filter(username=user.username),
            widget=forms.HiddenInput,
        )


class PersonalDataUpdateForm(forms.ModelForm):
    """PersonalDataUpdateForm, used to update a personal data.

    Args:
        user (User): user model
    Fields:
        user: user model
        first_name: first name field
        last_name: last name field
        birth_day: birth day field
        sex: sex field
    """
    class Meta:
        model = PersonalData
        fields = ("first_name", "last_name", "birth_day", "sex")


class PersonalTimeStampDataCreateForm(forms.ModelForm):
    """PersonalTimeStampDataCreateForm, used to create a new personal time stamp data.

    Args:
        user (User): user model
        personal_data (PersonalData): personal data model
    Fields:
        personal_data: personal data model
        weight: weight field
        height: height field
        cardiac_pulse: cardiac pulse field
        glucose: glucose field
        cholesterol: cholesterol field
    """
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
        """Initialize the form.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.            
        """
        user: User = kwargs.pop("user", "")
        super().__init__(*args, **kwargs)
        self.fields["personal_data"] = forms.ModelChoiceField(
            queryset=PersonalData.objects.filter(user=user),
            widget=forms.HiddenInput,
        )


class PersonalTimeStampDataUpdateForm(forms.ModelForm):
    """PersonalTimeStampDataUpdateForm, used to update a personal time stamp data.

    Args:
        user (User): user model
    Fields:
        weight: weight field
        height: height field
        cardiac_pulse: cardiac pulse field
        glucose: glucose field
        cholesterol: cholesterol field
    """
    class Meta:
        model = PersonalTimeStampData
        fields = (
            "weight",
            "height",
            "cardiac_pulse",
            "glucose",
            "cholesterol",
        )
