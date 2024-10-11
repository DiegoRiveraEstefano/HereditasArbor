import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PersonalsConfig(AppConfig):
    name = "hereditasarbor.apps.personals"
    verbose_name = _("Personal")

    def ready(self):
        with contextlib.suppress(ImportError):
            import hereditasarbor.apps.personals.signals  # noqa: F401
