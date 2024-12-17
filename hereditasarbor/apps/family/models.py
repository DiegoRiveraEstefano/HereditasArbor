
from django.db import models
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from hereditasarbor.apps.users.models import User


class FamilyTree(models.Model):

    """family tree model, used to store family trees.

    Fields: owner, last_update

    Description: owner: owner model, last_update: last update date

    """

    owner = models.OneToOneField(
        User,
        verbose_name=_("Arbol Dueño"),
        on_delete=models.CASCADE,
        related_name="family_tree",
    )

    last_update = models.DateTimeField(
        _("Ultimo Cambio"),
        auto_now=True,
        auto_now_add=False,
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
        """Get the size of the family tree.

        Returns:
            int: The size of the family tree.
        """
        return len(self.get_all_family())

    def get_all_family(self) -> QuerySet:
        """Get all familiar of the family tree.

        Returns:
            QuerySet: All familiar of the family tree.
        """
        return self.familiar.all()



class Familiar(models.Model):

    """familiar model, used to store familiars.

    Fields: tree, name, sex, relation_type, birth_date, death, death_type, death_date, weight, height

    Description: tree: tree model, name: name, sex: sex, relation_type: relation type, birth_date: birth date, death: death, death_type: death type, death_date: death date, weight: weight, height: height

    """

    sexs = ((1, "Femenino"), (0, "Masculino"))

    relation_types = (
        ("father", "Padre"),  # distance 1
        ("mother", "Madre"),  # distance 1
        ("brother", "Hermano"),  # distance 2
        ("sister", "Hermana"),  # distance 2
        ("son", "Hijo"),  # distance 1
        ("daughter", "Hija"),  # distance 1
        ("grandfather", "Abuelo"),  # distance 3
        ("grandmother", "Abuela"),  # distance 3
        ("uncle", "Tío"),  # distance 4
        ("aunt", "Tía"),  # distance 4
        ("cousin", "Primo"),  # distance 5
        ("nephew", "Sobrino"),  # distance 6
        ("niece", "Sobrina"),  # distance 6
        ("other", "Otro"),  # distance 7
        ("null", "null"),  # Sin relación conocida o irrelevante
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

    def get_all_diseases(self) -> QuerySet:
        """Get all diseases of the familiar.

        Returns:
            QuerySet: All diseases of the familiar. 
        """
        return self.diseases.all()
