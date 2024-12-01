from django.forms.widgets import DateInput


class TailwindDateInput(DateInput):
    template_name = "components/date_input.html"
