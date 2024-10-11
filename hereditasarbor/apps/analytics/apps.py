import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AnalyticsConfig(AppConfig):
    name = "hereditasarbor.apps.analytics"
    verbose_name = _("Analytics")

    def ready(self):
        with contextlib.suppress(ImportError):
            import hereditasarbor.apps.analytics.signals  # noqa: F401
