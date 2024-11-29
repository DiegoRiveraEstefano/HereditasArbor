from functools import lru_cache

from celery import shared_task
from numba import float32
from numba import int16
from numba import int32
from numba import jit
from numba import njit

from config.celery_app import app
from hereditasarbor.apps.analytics.tasks.utils import disease_degradations
from hereditasarbor.apps.diseases.models import Disease
from hereditasarbor.apps.family.models import Familiar
from hereditasarbor.apps.family.models import FamilyTree

# const for the calcs
WC = 2.0
WCH = 3.0
WS = 0.5
WP = 10.0

# theoretical const to norm the score to chance
W_MAX = 3.50
W_MIN = 0.05
W_NORM = 3.45


@lru_cache(maxsize=256)
@njit(float32(float32, int16, int16), fastmath=True)
def calc_inheritance_score(
    chance: float,
    count: int,
    degradation_sum: int,
) -> float:
    return ((WC * count) + (WCH * (chance / 100))) / (1 + (WS * degradation_sum))


@lru_cache(maxsize=256)
@njit(float32(float32, int16), fastmath=True)
def calc_error_delta(score: float, degradation_sum: int = 0) -> float:
    return (WS * degradation_sum) - score


@lru_cache(maxsize=256)
@njit(float32(float32), fastmath=True)
def score_to_chance(score: float) -> float:
    return (score - W_MIN) / W_NORM


@jit(forceobj=True)
def extract_data(tree_pk: int) -> dict[int, dict[str, int | dict]]:
    data: dict[int, dict[str, int | Disease]] = {}
    tree = FamilyTree.objects.get(pk=tree_pk)
    for _familiar in tree.get_all_family():
        familiar: Familiar = _familiar
        degradation = disease_degradations[familiar.relation_type]
        for family_disease in familiar.get_all_diseases():
            disease: Disease = family_disease.disease
            if not disease.endogena:
                continue
            if disease.pk not in data:
                data[disease.pk] = {
                    "count": 0,
                    "degradation_sum": 0,
                    "disease": {
                        "name": disease.name,
                        "chance": disease.chance,
                        "pk": disease.pk,
                    },
                }
            data[disease.pk]["count"] += 1
            data[disease.pk]["degradation_sum"] += degradation
    return data


@app.task()
def get_data_per_family(
    tree_pk: int,
) -> dict[int, dict[str, int | Disease | float]]:
    data: dict[int, dict[str, int | Disease]] = extract_data(tree_pk=tree_pk)
    for disease_data in data:
        data[disease_data]["score"] = calc_inheritance_score(
            chance=data[disease_data]["disease"]["chance"],
            count=data[disease_data]["count"],
            degradation_sum=data[disease_data]["degradation_sum"],
        )

        data[disease_data]["chance_from_score"] = score_to_chance(
            score=data[disease_data]["score"],
        )

        data[disease_data]["display_score"] = int(data[disease_data]["score"])
        data[disease_data]["percentage"] = int(
            data[disease_data]["chance_from_score"] * 100
        )
        data[disease_data]["delta"] = int(
            abs(
                calc_error_delta(
                    score=data[disease_data]["score"],
                    degradation_sum=data[disease_data]["degradation_sum"],
                )
                * 10
            )
        )
    return data
