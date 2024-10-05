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
    template_name = ".html"


class FamiliarListView(ListView, LoginRequiredMixin):
    model = Familiar
    template_name = ".html"


class FamiliarCreateView(CreateView, LoginRequiredMixin):
    model = Familiar
    template_name = ".html"
    form_class = FamiliarForm
    success_url = reverse("familiar_list")


class FamilyTreeDetailView(DetailView, LoginRequiredMixin):
    model = FamilyTree
    template_name = ".html"
