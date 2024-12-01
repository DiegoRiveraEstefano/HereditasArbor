from django.forms import DateField

from .widgets import TailwindDateInput


class TailwindDateField(DateField):
    widget = TailwindDateInput
