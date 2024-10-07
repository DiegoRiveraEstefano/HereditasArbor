from collections.abc import Iterable

from django.db import models
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from hereditasarbor.apps.diseases.models import Disease
from hereditasarbor.apps.family.models import Familiar
from hereditasarbor.apps.users.models import User


class FamiliarDiseases(models.Model):
    """_summary_

    Links:
        https://stackoverflow.com/questions/5708650/how-do-i-add-a-foreign-key-field-to-a-modelform-in-django

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """

    familiar = models.ForeignKey(
        Familiar,
        verbose_name=_("Enfermedad Familiar"),
        on_delete=models.CASCADE,
        related_name="diseases",
    )

    disease = models.ForeignKey(
        Disease,
        verbose_name=_("Enfermedad"),
        on_delete=models.CASCADE,
        related_name="persons",
    )

    class Meta:
        ordering = ["familiar"]
        verbose_name = _("FamiliarDiseases")
        verbose_name_plural = _("FamiliarDiseasess")

    def __str__(self):
        return f"FamiliarDiseases(pk={self.pk}, familiar={self.familiar}, disease={self.disease})"

    def get_absolute_url(self):
        return reverse("family-diseases:detail", kwargs={"pk": self.pk})
