from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from .models import Disease
from .models import DiseaseCategory


class DiseaseDetailView(DetailView):

    """DiseaseDetailView, used to display a disease detail.

    Args:
        model (Disease): disease model
        template_name (str): template name
        slug_field (str): slug field
        slug_url_kwarg (str): slug url kwarg
    """

    model = Disease
    template_name = "diseases/views/diseases_detail.html"
    slug_field = "pk"
    slug_url_kwarg = "pk"


disease_detail_view = DiseaseDetailView.as_view()
