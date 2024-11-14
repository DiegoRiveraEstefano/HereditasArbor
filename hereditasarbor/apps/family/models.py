from collections.abc import Iterable

from django.db import models
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from hereditasarbor.apps.diseases.models import Disease
from hereditasarbor.apps.users.models import User


class FamilyTree(models.Model):
    owner = models.OneToOneField(
        User,
        verbose_name=_("Arbol Dueño"),
        on_delete=models.CASCADE,
        related_name="family_tree",
    )

    class Meta:
        ordering = ["owner"]
        verbose_name = _("FamilyTree")
        verbose_name_plural = _("FamilyTrees")

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("FamilyTree_detail", kwargs={"pk": self.pk})

    @cached_property
    def size(self) -> int:
        return len(self.get_all_family())

    """@cached_property
    def different_diseases(self) -> Iterable[Disease]:
        return different_diseases_per_family(self)

    @cached_property
    def diseases_count(self) -> dict[int, dict[str, Disease | int]]:
        return count_per_disease_in_family(self)"""

    def get_all_family(self) -> QuerySet:
        return self.familiar.all()

    # def get_all_diseases(self) -> QuerySet:
    # return FamiliarDiseases.objects.filter(familiar__tree__pk=self.pk)


class Familiar(models.Model):
    sexs = ((1, "Femenino"), (0, "Masculino"))

    relation_types = (
        ("father", "Padre"),  # distance 1
        ("mother", "Madre"),  # distance 1
        ("cousin", "Primo"),  # distance 3
        ("brother", "Hermano"),  # distance 2
        ("null", "null"),
    )

    death_types = (
        ("null", "Null"),
        ("disease", "Enfermedad"),
        ("accident", "Accidente"),
    )

    tree = models.ForeignKey(
        FamilyTree,
        verbose_name=_(""),
        on_delete=models.CASCADE,
        related_name="familiar",
    )

    name = models.CharField(_("Nombre Familiar"), max_length=64, default="")

    sex = models.IntegerField(_("Sexo Familiar"), choices=sexs, default=0)

    relation_type = models.CharField(
        _("Tipo Relacion"), choices=relation_types, max_length=32, default="null"
    )

    birth_date = models.DateField(
        _("Fecha Nacimiento Familiar"), auto_now=False, auto_now_add=False, null=True
    )

    death = models.BooleanField(_("Defuncion"), default=False)

    death_type = models.CharField(
        _("Tipo Defuncion"), choices=death_types, max_length=64, default="null"
    )

    death_date = models.DateField(
        _("Fecha Muerte Familiar"), auto_now=False, auto_now_add=False, null=True
    )

    weight = models.IntegerField(_("Peso Familair kg"), default=60)

    height = models.IntegerField(_("Altura Familiar cm"), default=120)

    class Meta:
        ordering = ["tree", "birth_date"]
        verbose_name = _("Familiar")
        verbose_name_plural = _("Familiars")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("family:detail", kwargs={"pk": self.pk})

    def debug(self) -> str:
        return f"Familiar(pk={self.pk})"

    def get_all_diseases(self) -> Iterable[Disease]:
        return self.diseases.all()
