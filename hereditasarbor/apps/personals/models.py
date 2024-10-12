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


class PersonalTimeStampData(models.Model):
    personal_data = models.ForeignKey(
        PersonalData,
        verbose_name=_("Data Historica"),
        on_delete=models.CASCADE,
        related_name="datas",
    )

    added_data = models.DateField(
        _("Fecha de Añadido"), auto_now=False, auto_now_add=True
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

    def check_params(self, params: dict[str, dict[str, str]]) -> tuple[bool, int]:
        data = {
            "glucose": self.glucose,
        }
        """check with this data if the diseases param are true

        Args:
            params (dict): is a dict with a scheme similar to:
                {
                    "params": {
                        "glucose": "x >= 150",     
                    }
                }
                {
                    "params": [
                        {
                            "field": "glucose",
                            "validation": "lte",
                            "value": 150,
                        },
                        {
                            "field": "cardiac_pulse",
                            "validation": "gte",
                            "value": 120
                        },
                        {
                            "field": "cardiac_pulse",
                            "validation": "lte",
                            "value": 20
                        },
                    ]
                }

        Returns:
            bool: true if the condition is and false in other cases
            int: is a delta of magnitude
        """
        results = []
        deltas = []
        for key in params["params"].keys():
            if key not in data:
                continue
            if data[key] is None:
                results.append(False)
                deltas.append(0)
                continue
            expression = params["params"][key].replace("x", data[key])
            results.append(bool(eval(expression)))
            deltas.append(2)
        return all(results), sum(deltas) - len(params["params"].keys())
