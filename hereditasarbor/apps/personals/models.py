from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from hereditasarbor.apps.users.models import User


class PersonalData(models.Model):
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
        return self.datas.all()

    def get_last_time_stamp(self):
        return self.datas.order_by("-added_data").first()


class PersonalTimeStampData(models.Model):
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
        if bool(hasattr(self, attr)):
            return self.personal_data.__getattribute__(attr)
        return None
