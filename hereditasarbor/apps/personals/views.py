from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from .forms import PersonalDataCreateForm
from .forms import PersonalDataUpdateForm
from .forms import PersonalTimeStampDataCreateForm
from .forms import PersonalTimeStampDataUpdateForm
from .models import PersonalData
from .models import PersonalTimeStampData


class PersonalDataDetailView(DetailView, LoginRequiredMixin):
    """PersonalDataDetailView, used to display a personal data detail.

    Args:
        model (PersonalData): personal data model
        template_name (str): template name
    """

    model = PersonalData
    template_name = "personals/views/personal_detail.html"

    def get_object(self, queryset=None):
        return get_object_or_404(PersonalData, user=self.request.user)


personal_data_detail_view = PersonalDataDetailView.as_view()


class PersonalDataCreateView(CreateView, LoginRequiredMixin):
    """PersonalDataCreateView, used to create a new personal data.

    Args:
        model (PersonalData): personal data model
        template_name (str): template name
        form_class (PersonalDataCreateForm): personal data create form
    """

    model = PersonalData
    template_name = "personals/views/personal_create.html"
    form_class = PersonalDataCreateForm

    def get_success_url(self) -> str:
        return reverse("users:me")

    def get_initial(self) -> dict[str, Any]:
        return {"user": self.request.user.pk}

    def get_form_kwargs(self) -> dict[str, Any]:
        data = super().get_form_kwargs()
        data["user"] = self.request.user
        return data


personal_data_create_view = PersonalDataCreateView.as_view()


class PersonalDataUpdateView(UpdateView, LoginRequiredMixin):
    """PersonalDataUpdateView, used to update a personal data.

    Args:
        model (PersonalData): personal data model
        template_name (str): template name
        form_class (PersonalDataUpdateForm): personal data update form
    """

    model = PersonalData
    template_name = "personals/views/personal_edit.html"
    form_class = PersonalDataUpdateForm

    def get_object(self, queryset=...):
        return get_object_or_404(PersonalData, user=self.request.user)

    def get_success_url(self) -> str:
        return reverse("personal:me")


personal_data_update_view = PersonalDataUpdateView.as_view()


class PersonalTimeStampDataListView(ListView, LoginRequiredMixin):
    """PersonalTimeStampDataListView, used to list personal time stamp data.

    Args:
        model (PersonalTimeStampData): personal time stamp data model
        template_name (str): template name
    """

    model = PersonalTimeStampData
    template_name = "personals/views/persona_stamp_list.html"

    def get_queryset(self):
        return super().get_queryset().filter(personal_data__user=self.request.user)


personal_data_time_stamp_data_list_view = PersonalTimeStampDataListView.as_view()


class PersonalTimeStampDataDetailView(DetailView, LoginRequiredMixin):
    """PersonalTimeStampDataDetailView, used to display a personal time stamp data detail.

    Args:
        model (PersonalTimeStampData): personal time stamp data model
        template_name (str): template name
    """

    model = PersonalTimeStampData
    template_name = "personals/views/persona_stamp_detail.html"

    def get_queryset(self):
        return super().get_queryset().filter(personal_data__user=self.request.user)


personal_data_time_stamp_data_detail_view = PersonalTimeStampDataDetailView.as_view()


class PersonalTimeStampDataCreateView(CreateView, LoginRequiredMixin):
    """PersonalTimeStampDataCreateView, used to create a new personal time stamp data.

    Args:
        model (PersonalTimeStampData): personal time stamp data model
        template_name (str): template name
        form_class (PersonalTimeStampDataCreateForm): personal time stamp data create form
    """

    model = PersonalTimeStampData
    template_name = "personals/views/persona_stamp_create.html"
    form_class = PersonalTimeStampDataCreateForm

    def get_success_url(self) -> str:
        return reverse("personal:time_stamp-list")

    def get_initial(self):
        """Get the initial data of the view.

        Returns:
            dict[str, Any]: The initial data of the view.
        """

        data = super().get_initial()
        data["personal_data"] = get_object_or_404(
            PersonalData,
            user=self.request.user.pk,
        )
        return data

    def get_form_kwargs(self) -> dict[str, Any]:
        data = super().get_form_kwargs()
        data["user"] = self.request.user
        return data


personal_data_time_stamp_data_create_view = PersonalTimeStampDataCreateView.as_view()


class PersonalTimeStampDataUpdateView(UpdateView, LoginRequiredMixin):
    """PersonalTimeStampDataUpdateView, used to update a personal time stamp data.

    Args:
        model (PersonalTimeStampData): personal time stamp data model
        template_name (str): template name
        form_class (PersonalTimeStampDataUpdateForm): personal time stamp data update form
    """

    model = PersonalTimeStampData
    template_name = "personals/views/persona_stamp_edit.html"
    form_class = PersonalTimeStampDataUpdateForm

    def get_queryset(self):
        return super().get_queryset().filter(personal_data__user=self.request.user)


personal_data_time_stamp_data_update_view = PersonalTimeStampDataUpdateView.as_view()


class PersonalTimeStampDataDeleteView(DeleteView, LoginRequiredMixin):
    """PersonalTimeStampDataDeleteView, used to delete a personal time stamp data.

    Args:
        model (PersonalTimeStampData): personal time stamp data model
        template_name (str): template name
    """

    model = PersonalTimeStampData
    template_name = "temlates/personals/views/persona_stamp_delete.html"

    def get_success_url(self) -> str:
        return reverse("personal:time_stamp-list")

    def get_queryset(self):
        return super().get_queryset().filter(personal_data__user=self.request.user)


personal_data_time_stamp_data_delete_view = PersonalTimeStampDataDeleteView.as_view()
