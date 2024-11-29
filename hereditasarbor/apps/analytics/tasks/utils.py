import functools

disease_degradations = {
    "father": 1,
    "mother": 1,
    "son": 2,
    "daughter": 2,
    "brother": 3,
    "sister": 3,
    "grandfather": 3,
    "grandmother": 3,
    "uncle": 6,
    "aunt": 6,
    "cousin": 7,
    "nephew": 7,
    "niece": 8,
    "other": 9,
}


def memoize(max_length: int = 64):
    def decorator(func):
        memo = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if args in memo:
                return memo[args]
            else:
                rv = func(*args)
                if len(memo) > max_length:
                    memo.clear()
                memo[args] = rv
                return rv

        return wrapper

    return decorator


# --------------------
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

# todo: change this to read from a fixture file
disease_degradations = {
    "father": 1,
    "mother": 1,
    "brother": 2,
    "sister": 2,
    "grandfather": 3,
    "grandmother": 3,
    "uncle": 4,
    "aunt": 4,
    "cousin": 5,
    "son": 1,
    "daughter": 1,
    "nephew": 6,
    "niece": 6,
    "other": 7,  # Relación más distante o desconocida
}


def memoize(max_length: int = 64):
    def decorator(func):
        memo = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if args in memo:
                return memo[args]
            else:
                rv = func(*args)
                if len(memo) > max_length:
                    memo.clear()
                memo[args] = rv
                return rv

        return wrapper

    return decorator


@shared_task
def different_diseases_per_family(
    family_tree: FamilyTree,
) -> Iterable[FamiliarDiseases]:
    """return a iterable with all different diseases in a family tree
        this proccess can be large in a large family tree, and for that is a
        shared task

    Args:
        family_tree (FamilyTree): _description_

    Returns:
        Iterable[Disease]: _description_
    """
    familiar_list: Iterable[Familiar] = family_tree.get_all_family()
    diseases_list: set[Disease] = set()
    for familiar in familiar_list:
        for disease in familiar.get_all_diseases():
            diseases_list.add(disease)
    return diseases_list


@shared_task
def count_per_disease_in_family(
    family_tree: FamilyTree,
) -> dict[int, dict[str, Disease | int]]:
    familiar_list: Iterable[Familiar] = family_tree.get_all_family()
    diseases_list: dict[int, dict[str, Disease | int]] = {}
    for familiar in familiar_list:
        for disease in familiar.get_all_diseases():
            if disease.disease.pk not in diseases_list:
                diseases_list[disease.disease.pk] = {"disease": disease, "count": 1}
            else:
                diseases_list[disease.disease.pk]["count"] = (
                    1 + diseases_list[disease.disease.pk]["count"]
                )
    return diseases_list


@shared_task
def calculate_chance_of_disease(disease: Disease, family_tree: FamilyTree) -> int:
    """for now this return a "score" that it is a sum of all familiar with this disease,
        this hav a degradation for distance in mind

        = sum ( 10 - x.disease_degradation )

        for a large tree this number can be "large"

        number below or equal zero are not disease chance

        9 is a chance of. like a 35%
        18 is a chance of a 75%
        more that 20 is a 100% of chance

        this number for now are only for testing, and need to be investigated

    Args:
        disease (Disease): _description_
        family_tree (FamilyTree): _description_

    Returns:
        int: score of the chance of disease
    """
    """sum(
        (
            10 - disease_degradations[x.familiar.relation_type]
            for x in filter(
                lambda x: x.disease.pk == disease.pk and x.disease.endogena,
                family_tree.get_all_diseases(),
            )
        ),
    )"""
    score = 0
    for _family_disease in different_diseases_per_family(family_tree):
        family_disease: FamiliarDiseases = _family_disease
        if (  # todo: refactor this to use filter expression.
            family_disease.disease.pk != disease.pk
            or not family_disease.disease.endogena
        ):
            continue
        disease_degradation = (  # todo: add the count as a factor of risk in the calc
            10 - disease_degradations[family_disease.familiar.relation_type]
        )
        score += disease_degradation

    return score


@shared_task
@memoize(max_length=256)
def convert_score_to_chance(score: int) -> float:
    """NO TESTED

    Args:
        score (int): _description_

    Returns:
        float: _description_
    """
    if score <= 8:
        chance = score / 9  # Linearly increases from 0 to 1 between 0 and 8
    elif score <= 17:
        chance = (
            0.8 + (score - 9) / 9
        )  # Linearly increases from 0.8 to 1 between 9 and 17
    else:
        chance = 1.0  # 100% chance for numbers greater than 19

    return chance


@shared_task
def calc_diseas_from_params(
    disease: Disease,
    personal_data: PersonalData,
) -> tuple[bool, int]:
    params: QuerySet[DiseasesParams] = disease.get_params()
    last_personal_time_stamp: QuerySet[PersonalTimeStampData] = (
        personal_data.get_time_stamps().values().latest()
    )
    results = []
    for x in params:
        try:
            results.append(
                x.check_expression(value=last_personal_time_stamp[x.personal_field])
            )
        except:
            continue

    boleans = []
    deltas = []
    for x in results:
        boleans.append(x[0])
        deltas.append(abs(x[1]))
    mean = np.mean(deltas)
    try:
        mean = int(mean)
    except:
        mean = 0
    return all(boleans), mean


@shared_task
def get_deltas_from_disease(
    disease: Disease,
    personal_data: PersonalData,
) -> dict[int, dict[str, int | bool | DiseasesParams]]:
    params: QuerySet[DiseasesParams] = disease.get_params()
    last_personal_time_stamp: QuerySet[PersonalTimeStampData] = (
        personal_data.get_time_stamps().values().latest()
    )
    data = {}
    for x in params:
        try:
            result = x.check_expression(
                value=last_personal_time_stamp[x.personal_field]
            )
        except:
            continue
        data[x.pk] = {
            "param": x,
            "definition": result[0],
            "delta": abs(result[1]),
        }
    return data
