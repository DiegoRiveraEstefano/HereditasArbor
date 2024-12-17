from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class DiseaseCategory(models.Model):
    """disease category model, used to store disease categories.

    fields: name, description

    """
    name = models.CharField(
        _("Nombre Categoria"), max_length=64
    )  # Field to store the name of the disease category

    description = models.CharField(
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
    """disease model, used to store diseases.

    fields: name, description, endogena, chance, category

    """

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
        return self.name

    def get_absolute_url(self):
        """Get the absolute url of the disease.

        Returns:
            str: The absolute url of the disease.
        """
        return reverse("diseases:detail", kwargs={"pk": self.pk})

    def get_params(self) -> models.QuerySet:
        """Get the disease parameters.

        Returns:
            QuerySet: The disease parameters.
        """
        return self.params.all()


class DiseasesParams(models.Model):

    """disease parameters model, used to store disease parameters.

    fields: disease, personal_field, value, operation

    operations: lte, lt, gte, gt

    """


    fields = (("glucose", "Glucosa"), ("cholesterol", "Colesterol"))
    operations = (
        ("lte", "Less Than Equal"),
        ("lt", "Less Than"),
        ("gte", "Greater Than Equal"),
        ("gt", "Greater Than"),
    )

    disease = models.ForeignKey(
        Disease,
        verbose_name=_("Enfermedad"),
        on_delete=models.CASCADE,
        related_name="params",
    )

    # todo: change this name
    personal_field = models.CharField(_("Campo"), choices=fields, max_length=32)
    value = models.IntegerField(_("Valor Limite"), default=0)
    operation = models.CharField(
        _("Tipo de Validacion"), choices=operations, max_length=12
    )

    class Meta:
        verbose_name = _("DiseasesParams")
        verbose_name_plural = _("DiseasesParamss")

    def __str__(self):
        return f"DiseasesParams(disease={self.disease}, personal_field={self.personal_field}, operation={self.operation}, value={self.value})"

    def get_absolute_url(self):
        return reverse("DiseasesParams_detail", kwargs={"pk": self.pk})

    def check_expression(self, value: float) -> tuple[bool, float]:
        delta = value - self.value
        match self.operation:
            case "lte":
                return value <= self.value, delta
            case "lt":
                return value < self.value, delta
            case "gte":
                return value >= self.value, delta
            case "gt":
                return value > self.value, delta
