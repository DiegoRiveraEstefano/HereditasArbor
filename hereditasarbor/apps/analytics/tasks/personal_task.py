from collections.abc import Iterable
from functools import lru_cache

import numba
from celery import shared_task
from numba import float32
from numba import int16
from numba import int32
from numba import jit
from numba import njit

from hereditasarbor.apps.diseases.models import Disease
from hereditasarbor.apps.diseases.models import DiseaseCategory
from hereditasarbor.apps.diseases.models import DiseasesParams
from hereditasarbor.apps.family.models import Familiar
from hereditasarbor.apps.family.models import FamilyTree
from hereditasarbor.apps.family_diseases.models import FamiliarDiseases
from hereditasarbor.apps.personals.models import PersonalData
from hereditasarbor.apps.personals.models import PersonalTimeStampData


@jit(nopython=False, looplift=True, forceobj=True, cache=True)
def parse_expression(
    value: float,
    operation: str,
    expected: float,
) -> tuple[bool, float]:
    """parse an expression

    Args:
        value (float): is the value to check
        operation (str): is the operation to check
        expected (float): is the expected value
    
    Description:
        - parse an expression
        - return a tuple with the result and the delta

    Returns:
        tuple[bool, float]: is a tuple with the result and the delta
    """
    delta: float = abs(value - expected)
    match operation:
        case "lte":
            return value <= expected, delta
        case "lt":
            return value < expected, delta
        case "gte":
            return value >= expected, delta
        case "gt":
            return value > expected, delta
    return False, 0


@jit(nopython=False, looplift=True, forceobj=True)
def check_params(
    disease: Disease,
    personal_data: PersonalData,
) -> dict[str, dict[str, bool | int]]:
    """check if the disease is present in the personal data

    Args:
        disease (Disease): is a disease to check
        personal_data (PersonalData): is the personal data to check

    Returns:
        dict[str, dict[str, bool | int]]: is a dictionary with the params and the result
    """
    data: dict[str, dict[str, bool | int]] = {}
    for param in disease.get_params():
        personal_field = personal_data.get_last_time_stamp().get_field(
            param.personal_field
        )
        if personal_field is None:
            continue
        is_true, delta = parse_expression(
            value=personal_field,
            operation=param.operation,
            expected=param.value,
        )
        data[param.personal_field] = {
            "is_true": is_true,
            "delta": delta,
        }
    return data

#@jit(nopython=False, looplift=True, forceobj=True)
def calc_all_diseases(
    personal_data: PersonalData,
    endogenous: bool = False,
) -> dict[str, dict[str | int, dict[str, bool | int]]]:

    """Calculate all diseases.

    Args:
        personal_data (PersonalData): The personal data.
        endogenous (bool, optional): Whether to calculate only endogenous diseases. Defaults to False.

    Returns:
        dict[str, dict[str | int, dict[str, bool | int]]]: The calculated diseases.
    """

    data: dict[str, dict[str | int, dict[str, bool | int]]] = {}

    diseases = Disease.objects.filter(endogena=endogenous)
    for disease in diseases:
        result = check_params(disease, personal_data)
        print(disease, result)
        # all params are false
        if not any(x["is_true"] for x in result.values()):
            continue
        data["diseases"][disease.pk] = check_params(disease, personal_data)
    return data
