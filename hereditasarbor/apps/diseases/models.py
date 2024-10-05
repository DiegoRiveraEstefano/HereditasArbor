from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class DiseaseCategory(models.Model):
    name = models.CharField(_("Nombre Categoria"), max_length=64)

    decription = models.CharField(_("Descripcion Categoria"), max_length=128)

    class Meta:
        verbose_name = _("DiseaseCategory")
        verbose_name_plural = _("DiseaseCategorys")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("DiseaseCategory_detail", kwargs={"pk": self.pk})


class Disease(models.Model):
    name = models.CharField(_("Nombre Enfermedad"), max_length=64)

    description = models.CharField(_("Descripcion Enfermedad"), max_length=256)

    endogena = models.BooleanField(_("Enfermdad Endogena"))

    chance = models.FloatField(_("Probabilidad Hereditaria"))

    category = models.ForeignKey(
        DiseaseCategory,
        verbose_name=_("Categoria Enfermedad"),
        on_delete=models.CASCADE,
        related_name="diseases",
    )

    class Meta:
        verbose_name = _("Disease")
        verbose_name_plural = _("Diseases")

    def __str__(self):
        return self.pk

    def get_absolute_url(self):
        return reverse("Disease_detail", kwargs={"pk": self.pk})
