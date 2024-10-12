from typing import Any

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


class AnalyticsIndexView(TemplateView, LoginRequiredMixin):
    template_name = "analytics/analytics_resume.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["tree"] = self.request.user.family_tree
        data["count_per_disease"] = count_per_disease_in_family(
            self.request.user.family_tree,
        )
        for disease in data["count_per_disease"]:
            data["count_per_disease"][disease]["risk"] = calculate_chance_of_disease(
                family_tree=self.request.user.family_tree,
                disease=data["count_per_disease"][disease]["disease"].disease,
            )
        data["b"] = calc_diseas_from_params(
            disease=data["count_per_disease"][2]["disease"].disease,
            personal_data=self.request.user.get_personal_data(),
        )
        return data


analytics_index_view = AnalyticsIndexView.as_view()
