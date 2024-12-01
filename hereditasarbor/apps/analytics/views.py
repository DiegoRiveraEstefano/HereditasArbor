from typing import TYPE_CHECKING

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView

from hereditasarbor.apps.analytics.models import Analytic
from hereditasarbor.apps.analytics.tasks.view_tasks import get_analytic_or_create
from hereditasarbor.apps.family.models import FamilyTree
from hereditasarbor.apps.personals.models import PersonalData

from .models import Analytic
from .models import AnalyticPersonal
from .models import AnalyticTree

if TYPE_CHECKING:
    from collections.abc import Iterable


class AnalyticsCreateView(TemplateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Analytic
    template_name = "analytics/analytics_detail.html"

    def test_func(self):
        assert self.request.user.is_authenticated
        if not self.request.user.has_personal_data:
            return False
        return self.request.user.get_personal_data().get_time_stamps().count() != 0

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            return HttpResponseRedirect(reverse("personal:time_stamp-create"))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        assert self.request.user.is_authenticated
        data = super().get_context_data(**kwargs)

        analytic, created = get_analytic_or_create(user=self.request.user)
        data["analytic"] = analytic
        data["created"] = created
        return data


analytics_create_view = AnalyticsCreateView.as_view()


class AnalyticsDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Analytic
    template_name = "analytics/analytics_detail.html"
    queryset = Analytic.objects.all()
    context_object_name = "analytic"
    slug_field = "pk"
    slug_url_kwarg = "pk"

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


analytics_detail_view = AnalyticsDetailView.as_view()


class AnalyticsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Analytic
    template_name = "analytics/analytics_list.html"

    def test_func(self):
        assert self.request.user.is_authenticated
        if not self.request.user.has_personal_data:
            return False
        return self.request.user.get_personal_data().get_time_stamps().count() != 0

    def get_queryset(self):
        assert self.request.user.is_authenticated
        return Analytic.objects.filter(user=self.request.user)


analytics_list_view = AnalyticsListView.as_view()
