import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DiseasesConfig(AppConfig):
    name = "hereditasarbor.apps.diseases"
    verbose_name = _("Diseases")

    def ready(self):
        with contextlib.suppress(ImportError):
            import hereditasarbor.apps.diseases.signals  # noqa: F401
