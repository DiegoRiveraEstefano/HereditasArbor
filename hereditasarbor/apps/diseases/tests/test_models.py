from hereditasarbor.apps.diseases.models import Disease
from hereditasarbor.apps.diseases.models import DiseaseCategory


def test_disease_get_absolute_url(disease: Disease):
    assert disease.get_absolute_url() == f"/diseases/{disease.pk}/"
