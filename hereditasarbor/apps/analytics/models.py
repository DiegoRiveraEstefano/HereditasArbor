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

    class Meta:
        verbose_name = _("Analytic")
        verbose_name_plural = _("Analytics")

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("Analytic_detail", kwargs={"pk": self.pk})

    def get_tree_result(self):
        return self.analytic_tree.result

    def get_personal_result(self):
        return self.analytic_personal.result


class AnalyticTree(models.Model):
    analytic = models.OneToOneField(
        Analytic,
        verbose_name=_("Analytic"),
        on_delete=models.CASCADE,
        related_name="analytic_tree",
    )

    last_change = models.DateTimeField(
        _("Ultimo Cambio Arbol Familiar"),
        auto_now=False,
        auto_now_add=False,
        null=False,
        unique=False,
    )

    result = models.JSONField(_("Resultados herencia"), null=True)

    class Meta:
        verbose_name = _("AnalyticTree")
        verbose_name_plural = _("AnalyticTrees")

    def __str__(self):
        return str(self.pk)


class AnalyticPersonal(models.Model):
    analytic = models.OneToOneField(
        Analytic,
        verbose_name=_("Analytic"),
        on_delete=models.CASCADE,
        related_name="analytic_personal",
    )

    last_change = models.DateTimeField(
        _("Ultimo Cambio Arbol Familiar"),
        auto_now=False,
        auto_now_add=False,
        null=False,
        unique=False,
    )

    result = models.JSONField(_("Resultados Personales"), null=True)

    class Meta:
        verbose_name = _("AnalyticPersonal")
        verbose_name_plural = _("AnalyticPersonals")

    def __str__(self):
        return str(self.pk)
