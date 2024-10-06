from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from hereditasarbor.apps.family.models import Familiar
from hereditasarbor.apps.family.models import FamiliarDiseases
from hereditasarbor.apps.family.models import FamilyTree

from .forms import FamiliarDiseasesForm
from .forms import FamiliarForm


class FamiliarDetailView(DetailView, LoginRequiredMixin):
    model = Familiar
    template_name = "family_details.html"


familiar_detail_view = FamiliarDetailView.as_view()


class FamiliarListView(ListView, LoginRequiredMixin):
    model = Familiar
    template_name = "family_list.html"


familiar_list_view = FamiliarListView.as_view()


class FamiliarCreateView(CreateView, LoginRequiredMixin):
    model = Familiar
    template_name = "family_create.html"
    form_class = FamiliarForm
    # success_url =

    def get_success_url(self) -> str:
        return reverse("family:list")


familiar_create_view = FamiliarCreateView.as_view()


class FamiliarUpdateView(UpdateView, LoginRequiredMixin):
    model = Familiar
    template_name = "family_update.html"

    def get_success_url(self) -> str:
        return reverse("family:list", kwargs={"pk": self.get_object().pk})


familiar_update_view = FamiliarUpdateView.as_view()


class FamiliarDeleteView(DeleteView, LoginRequiredMixin):
    model = Familiar
    template_name = "family_delete.html"


familiar_delete_view = FamiliarDeleteView.as_view()


class FamilyTreeDetailView(DetailView, LoginRequiredMixin):
    model = FamilyTree
    template_name = ".html"


class FamiliarDiseasesDetailView(DetailView, LoginRequiredMixin):
    model = FamiliarDiseases
    template_name = ".html"
