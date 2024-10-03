import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "hereditasarbor.apps.familiars"
    verbose_name = _("Users")

    def ready(self):
        with contextlib.suppress(ImportError):
            import hereditasarbor.apps.familiars.signals  # noqa: F401
