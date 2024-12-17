from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from hereditasarbor.apps.family.forms import FamiliarForm
from hereditasarbor.apps.family.forms import FamiliarUpdateForm
from hereditasarbor.apps.family.models import Familiar
from hereditasarbor.apps.family.models import FamilyTree


class FamiliarDetailView(DetailView, LoginRequiredMixin):
    """FamiliarDetailView, used to display a familiar detail.

    Args:
        model (Familiar): familiar model
        template_name (str): template name
        slug_field (str): slug field
        slug_url_kwarg (str): slug url kwarg
    """
    model = Familiar
    template_name = "family/views/family_details.html"
    slug_field = "pk"
    slug_url_kwarg = "pk"


familiar_detail_view = FamiliarDetailView.as_view()


class FamiliarListView(ListView, LoginRequiredMixin):
    """FamiliarListView, used to list familiars.

    Args:
        model (Familiar): familiar model
        template_name (str): template name
    """
    model = Familiar
    template_name = "family/views/family_list.html"

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(tree__owner=self.request.user)


familiar_list_view = FamiliarListView.as_view()


class FamiliarCreateView(CreateView, LoginRequiredMixin):
    """FamiliarCreateView, used to create a new familiar.

    Args:
        model (Familiar): familiar model
        template_name (str): template name
        form_class (FamiliarForm): familiar form
    """
    model = Familiar
    template_name = "family/views/family_create.html"
    form_class = FamiliarForm

    def get_initial(self) -> dict[str, Any]:
        return {"tree": self.request.user.family_tree.pk}

    def get_form_kwargs(self) -> dict[str, Any]:
        data = super().get_form_kwargs()
        data["user"] = self.request.user
        return data

    def get_success_url(self) -> str:
        return reverse("family:list")


familiar_create_view = FamiliarCreateView.as_view()


class FamiliarUpdateView(UpdateView, LoginRequiredMixin):

    """FamiliarUpdateView, used to update a familiar.

    Args:
        model (Familiar): familiar model
        template_name (str): template name
        slug_field (str): slug field
        slug_url_kwarg (str): slug url kwarg
        form_class (FamiliarUpdateForm): familiar update form
    """

    model = Familiar
    template_name = "family/views/family_update.html"
    slug_field = "pk"
    slug_url_kwarg = "pk"
    form_class = FamiliarUpdateForm

    def get_success_url(self) -> str:
        return reverse("family:detail", kwargs={"pk": self.get_object().pk})


familiar_update_view = FamiliarUpdateView.as_view()


class FamiliarDeleteView(DeleteView, LoginRequiredMixin):

    """FamiliarDeleteView, used to delete a familiar.

    Args:
        model (Familiar): familiar model
        template_name (str): template name
    """

    model = Familiar
    template_name = "family/views/family_delete.html"

    def get_success_url(self) -> str:
        return reverse("family:list")


familiar_delete_view = FamiliarDeleteView.as_view()


class FamilyTreeDetailView(DetailView, LoginRequiredMixin):

    """FamilyTreeDetailView, used to display a family tree detail.

    Args:
        model (FamilyTree): family tree model
        template_name (str): template name
    """

    model = FamilyTree
    template_name = ".html"
