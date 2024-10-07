from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class DiseaseCategory(models.Model):
    name = models.CharField(
        _("Nombre Categoria"), max_length=64
    )  # Field to store the name of the disease category

    decription = models.CharField(
        _("Descripcion Categoria"), max_length=128
    )  # Field to store the description of the disease category

    class Meta:
        verbose_name = _(
            "DiseaseCategory"
        )  # Human-readable name for a single object of the model
        verbose_name_plural = _(
            "DiseaseCategories"
        )  # Human-readable name for the collection of objects of the model

    def __str__(self):
        return (
            self.name
        )  # Returns a string representation of the disease category object

    def get_absolute_url(self):
        return reverse(
            "DiseaseCategory_detail", kwargs={"pk": self.pk}
        )  # Returns the canonical URL for an object, used in Django's templates for linking to specific instances of the model


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
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("diseases:detail", kwargs={"pk": self.pk})
