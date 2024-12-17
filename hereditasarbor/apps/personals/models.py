from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from hereditasarbor.apps.users.models import User


class PersonalData(models.Model):

    """personal data model, used to store personal data.

    Fields: user, last_update, first_name, last_name, birth_day, sex

    Description: user: user model, last_update: last update date, first_name: first name, last_name: last name, birth_day: birth day, sex: sex

    """

    sexs = ((1, "Femenino"), (0, "Masculino"))

    user = models.OneToOneField(
        User,
        verbose_name=_("Usuario Datos"),
        on_delete=models.CASCADE,
        related_name="personal_data",
    )

    last_update = models.DateTimeField(
        _("Ultimo Cambio"),
        auto_now=True,
        auto_now_add=False,
    )

    first_name = models.CharField(_("Primer Nombre"), max_length=64, default="")
    last_name = models.CharField(_("Apellido"), max_length=64, default="")

    birth_day = models.DateField(
        _("Fecha Nacimiento"), auto_now=False, auto_now_add=False, null=True
    )
    sex = models.IntegerField(_("Sexo"), choices=sexs, default=0)

    class Meta:
        verbose_name = _("Personal")
        verbose_name_plural = _("Personals")

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("personal:detail", kwargs={"pk": self.pk})

    def get_time_stamps(self) -> models.QuerySet:

        """Get the time stamps of the personal data.

        Returns:
            models.QuerySet: The time stamps of the personal data.
        """

        return self.datas.all()

    def get_last_time_stamp(self):

        """Get the last time stamp of the personal data.

        Returns:
            PersonalTimeStampData: The last time stamp of the personal data.
            None: If the personal data has no time stamps.
        """

        return self.datas.order_by("-added_data").first()


class PersonalTimeStampData(models.Model):

    """personal time stamp data model, used to store personal time stamp data.

    Fields: personal_data, added_data, weight, height, cardiac_pulse, glucose, cholesterol

    Description: personal_data: personal data model, added_data: added data, weight: weight, height: height, cardiac_pulse: cardiac pulse, glucose: glucose, cholesterol: cholesterol

    """

    personal_data = models.ForeignKey(
        PersonalData,
        verbose_name=_("Data Historica"),
        on_delete=models.CASCADE,
        related_name="datas",
    )

    added_data = models.DateField(
        _("Fecha de Añadido"),
        auto_now=False,
        auto_now_add=True,
    )

    weight = models.IntegerField(_("Peso"), default=70)
    height = models.IntegerField(_("Altura"), default=160)

    # todo: definir correctamente estos valores medicos
    cardiac_pulse = models.IntegerField(_("Frecuencia cardíaca"), null=True)

    glucose = models.IntegerField(_("Glucosa"), null=True)

    cholesterol = models.IntegerField(_("Colesterol"), null=True)

    class Meta:

        """Meta class for the PersonalTimeStampData model.

        Attributes:
            ordering (tuple[str, str]): Ordering for the model.
            get_latest_by (list[str]): Fields to use for latest by.
            verbose_name (str): Verbose name for the model.
            verbose_name_plural (str): Verbose name plural for the model.
            permissions (list[tuple[str, str]]): Permissions for the model.
        """

        ordering = ("added_data",)
        get_latest_by = ["pk", "added_data"]
        verbose_name = _("PersonalMedical")
        verbose_name_plural = _("PersonalMedicals")
        permissions = [
            ("has_personal_data", "Verify that the user has a personal data created"),
        ]

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("personal:time_stamp-detail", kwargs={"pk": self.pk})

    def get_field(self, attr: str):

        """Get the value of a field in the personal time stamp data.

        Args:
            attr (str): The name of the field.

        Returns:
            Any: The value of the field.
        """

        if bool(hasattr(self, attr)):
            return self.personal_data.__getattribute__(attr)
        return None
