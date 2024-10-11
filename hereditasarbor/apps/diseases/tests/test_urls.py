from django.urls import resolve
from django.urls import reverse

from hereditasarbor.apps.diseases.models import Disease
from hereditasarbor.apps.diseases.models import DiseaseCategory


def test_detail(disease: Disease):
    assert (
        reverse("diseases:detail", kwargs={"pk": disease.pk})
        == f"/diseases/{disease.pk}/"
    )
    assert resolve(f"/diseases/{disease.pk}/").view_name == "diseases:detail"
