from collections.abc import Iterable

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.base import Model as Model
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from hereditasarbor.apps.analytics.models import Analytic
from hereditasarbor.apps.analytics.tasks import calc_diseas_from_params
from hereditasarbor.apps.analytics.tasks import calculate_chance_of_disease
from hereditasarbor.apps.analytics.tasks import convert_score_to_chance
from hereditasarbor.apps.analytics.tasks import count_per_disease_in_family
from hereditasarbor.apps.analytics.tasks import different_diseases_per_family
from hereditasarbor.apps.analytics.tasks import get_deltas_from_disease
from hereditasarbor.apps.diseases.models import Disease
from hereditasarbor.apps.diseases.models import DiseasesParams


class AnalyticsIndexView(TemplateView, LoginRequiredMixin):
    template_name = "analytics/analytics_resume.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["tree"] = self.request.user.family_tree
        data["diseases"] = count_per_disease_in_family(
            self.request.user.family_tree,
        )
        for disease in data["diseases"]:
            data["diseases"][disease]["risk"] = calculate_chance_of_disease(
                family_tree=self.request.user.family_tree,
                disease=data["diseases"][disease]["disease"].disease,
            )
        for disease in data["diseases"]:
            data["diseases"][disease]["params"] = calc_diseas_from_params(
                personal_data=self.request.user.get_personal_data(),
                disease=data["diseases"][disease]["disease"].disease,
            )
        return data


analytics_index_view = AnalyticsIndexView.as_view()


class AnalyticsDetailView(TemplateView):
    template_name = "analytics/analytics_detail.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        disease: Disease = get_object_or_404(Disease, pk=kwargs["pk"])
        params: Iterable[DiseasesParams] = disease.get_params()
        """
        result scheme = {
            "disaes_pk": {
                "param": DiseasesParams,
                "definition": bool,
                "delta": int,
            }
        }
        """
        result: dict[int, dict[str, int | bool | DiseasesParams]] = (
            get_deltas_from_disease(
                disease=disease,
                personal_data=self.request.user.get_personal_data(),
            )
        )
        data["disease"] = disease
        data["disease_params"] = params
        data["result"] = result
        return data


analytics_detail_view = AnalyticsDetailView.as_view()
