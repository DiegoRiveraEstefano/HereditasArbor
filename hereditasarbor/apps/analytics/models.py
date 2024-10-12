from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from hereditasarbor.apps.users.models import User


class Analytic(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_("Usuario"),
        on_delete=models.CASCADE,
        related_name="analytics",
    )

    created_at = models.DateField(
        _("Fecha de Creacion"),
        auto_now=False,
        auto_now_add=True,
    )

    # json enconded result
    result = models.JSONField(_("Resultados"), null=True)

    class Meta:
        verbose_name = _("Analytic")
        verbose_name_plural = _("Analytics")

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("Analytic_detail", kwargs={"pk": self.pk})
