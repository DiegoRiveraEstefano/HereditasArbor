import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "hereditasarbor.apps.family"
    verbose_name = _("Family")

    def ready(self):
        with contextlib.suppress(ImportError):
            import hereditasarbor.apps.family.signals  # noqa: F401
