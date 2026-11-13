from django.views.generic import DetailView

from .models import Disease


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
