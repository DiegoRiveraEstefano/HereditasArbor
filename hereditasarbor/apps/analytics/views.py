from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView

from hereditasarbor.apps.analytics.models import Analytic
from hereditasarbor.apps.analytics.tasks.view_tasks import get_analytic_or_create


class AnalyticsCreateView(TemplateView, LoginRequiredMixin, UserPassesTestMixin):
    """AnalyticsCreateView, used to create a new analytic.

    Args:
        model (Analytic): analytic model
        template_name (str): template name
    """

    model = Analytic
    template_name = "analytics/views/analytics_detail.html"

    def test_func(self):
        """Test function for the view.

        Returns:
            bool: True if the user has a personal data, False otherwise.
        """

        assert self.request.user.is_authenticated
        if not self.request.user.has_personal_data:
            return False
        return self.request.user.get_personal_data().get_time_stamps().count() != 0

    def dispatch(self, request, *args, **kwargs):
        """Dispatch the view.

        Args:
            request (HttpRequest): The request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The response object.
        """

        user_test_result = self.get_test_func()()
        if not user_test_result:
            return HttpResponseRedirect(reverse("personal:time_stamp-create"))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Get the context data of the view.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            dict[str, Any]: The context data of the view.
        """

        assert self.request.user.is_authenticated
        data = super().get_context_data(**kwargs)

        analytic, created = get_analytic_or_create(user=self.request.user)
        data["analytic"] = analytic
        data["created"] = created
        return data


analytics_create_view = AnalyticsCreateView.as_view()


class AnalyticsDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """AnalyticsDetailView, used to display an analytic detail.

    Args:
        model (Analytic): analytic model
        template_name (str): template name
        queryset (QuerySet[Any]): queryset
        context_object_name (str): context object name
        slug_field (str): slug field
        slug_url_kwarg (str): slug url kwarg
    """

    model = Analytic
    template_name = "analytics/views/analytics_detail.html"
    queryset = Analytic.objects.all()
    context_object_name = "analytic"
    slug_field = "pk"
    slug_url_kwarg = "pk"

    def test_func(self):
        """Test function for the view.

        Returns:
            bool: True if the user is the owner of the analytic, False otherwise.
        """
        return self.get_object().user == self.request.user

    def get_queryset(self):
        """Get the queryset of the view.

        Returns:
            QuerySet[Any]: The queryset of the view.
        """
        return super().get_queryset().filter(user=self.request.user)


analytics_detail_view = AnalyticsDetailView.as_view()


class AnalyticsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """AnalyticsListView, used to list analytics.

    Args:
        model (Analytic): analytic model
        template_name (str): template name
    """

    model = Analytic
    template_name = "analytics/views/analytics_list.html"

    def test_func(self):
        """Test function for the view.

        Returns:
            bool: True if the user has a personal data, False otherwise.
        """

        assert self.request.user.is_authenticated
        if not self.request.user.has_personal_data:
            return False
        return self.request.user.get_personal_data().get_time_stamps().count() != 0

    def get_queryset(self):
        """Get the queryset of the view.

        Returns:
            QuerySet[Any]: The queryset of the view.
        """

        assert self.request.user.is_authenticated
        return Analytic.objects.filter(user=self.request.user)


analytics_list_view = AnalyticsListView.as_view()
