import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FamilyDiseasesConfig(AppConfig):
    name = "hereditasarbor.apps.family_diseases"
    verbose_name = _("Family Diseases")

    def ready(self):
        with contextlib.suppress(ImportError):
            import hereditasarbor.apps.family_diseases.signals  # noqa: F401
