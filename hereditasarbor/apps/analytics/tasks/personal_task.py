import functools
from collections.abc import Iterable

import numpy as np
from celery import shared_task
from django.db.models import QuerySet
from hereditasarbor.apps.diseases.models import Disease
from hereditasarbor.apps.diseases.models import DiseaseCategory
from hereditasarbor.apps.diseases.models import DiseasesParams
from hereditasarbor.apps.family.models import Familiar
from hereditasarbor.apps.family.models import FamilyTree
from hereditasarbor.apps.family_diseases.models import FamiliarDiseases
from hereditasarbor.apps.personals.models import PersonalData
from hereditasarbor.apps.personals.models import PersonalTimeStampData


@shared_task
def calc_disease(disease: Disease, personal_data: PersonalData) -> tuple[bool, int]:
    pass


@shared_task
def calc_all_diseases(personal_data: PersonalData, endogenous=False) -> Iterable[tuple[bool, int]]:
    pass
