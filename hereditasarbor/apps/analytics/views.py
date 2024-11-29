from typing import TYPE_CHECKING

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from hereditasarbor.apps.analytics.tasks.tree_task import get_data_per_family
from hereditasarbor.apps.analytics.tasks.utils import calc_diseas_from_params
from hereditasarbor.apps.analytics.tasks.utils import calculate_chance_of_disease
from hereditasarbor.apps.analytics.tasks.utils import count_per_disease_in_family
from hereditasarbor.apps.analytics.tasks.utils import get_deltas_from_disease
from hereditasarbor.apps.diseases.models import Disease
from hereditasarbor.apps.diseases.models import DiseasesParams

if TYPE_CHECKING:
    from collections.abc import Iterable


class AnalyticsIndexView(UserPassesTestMixin, LoginRequiredMixin, TemplateView):
    template_name = "analytics/analytics_resume.html"

    def test_func(self):
        if not self.request.user.has_personal_data:
            return False
        return self.request.user.get_personal_data().get_time_stamps().count() != 0

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            return HttpResponseRedirect(reverse("personal:time_stamp-create"))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["diseases"] = get_data_per_family(
            tree_pk=self.request.user.family_tree.pk,
        )
        return data


analytics_index_view = AnalyticsIndexView.as_view()


class AnalyticsDetailView(TemplateView, LoginRequiredMixin):
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
