from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from hereditasarbor.apps.family.models import Familiar
from hereditasarbor.apps.family_diseases.models import FamiliarDiseases

from .forms import FamiliarDiseasesForm


class FamiliarDiseasesDetailView(DetailView, LoginRequiredMixin):
    model = FamiliarDiseases
    template_name = ".html"


family_diseases_detail_view = FamiliarDiseasesDetailView.as_view()


class FamilyDiseasesListView(ListView, LoginRequiredMixin):
    model = FamiliarDiseases
    template_name = "family_diseases/views/family_diseases_list.html"
    allow_empty = True

    # todo: optimize this two queries in one query
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return super().get_context_data(
            **kwargs,
            familiar=Familiar.objects.get(
                pk=self.kwargs["familiar"],
                tree__owner=self.request.user,
            ),
        )

    def get_queryset(self) -> QuerySet[Any]:
        Familiar.objects.none()
        return Familiar.objects.get(
            pk=self.kwargs["familiar"],
            tree__owner=self.request.user,
        ).diseases.all()


family_diseases_list_view = FamilyDiseasesListView.as_view()


class FamilyDiseasesCreateView(CreateView, LoginRequiredMixin):
    model = FamiliarDiseases
    template_name = "family_diseases/views/family_diseases_create.html"
    form_class = FamiliarDiseasesForm

    def get_success_url(self) -> str:
        return reverse(
            "family-diseases:list",
            kwargs={"familiar": self.kwargs["familiar"]},
        )

    def get_initial(self) -> dict[str, Any]:
        data = super().get_initial()
        data["familiar"] = self.kwargs["familiar"]
        return data

    def get_form_kwargs(self) -> dict[str, Any]:
        data = super().get_form_kwargs()
        data["user"] = self.request.user
        return data


family_diseases_create_view = FamilyDiseasesCreateView.as_view()


class FamilyDiseasesUpdateView(UpdateView, LoginRequiredMixin):
    model = FamiliarDiseases
    template_name = "family_diseases/views/family_diseases_update.html"


family_diseases_update_view = FamilyDiseasesUpdateView.as_view()


class FamilyDiseasesDeleteView(DeleteView, LoginRequiredMixin):
    model = FamiliarDiseases
    template_name = "family_diseases/views/family_diseases_delete.html"

    def get_success_url(self) -> str:
        return reverse(
            "family-diseases:list",
            kwargs={"familiar": self.kwargs["familiar"]},
        )


family_diseases_delete_view = FamilyDiseasesDeleteView.as_view()
