from typing import TYPE_CHECKING

from hereditasarbor.apps.analytics.models import Analytic
from hereditasarbor.apps.analytics.models import AnalyticPersonal
from hereditasarbor.apps.analytics.models import AnalyticTree
from hereditasarbor.apps.analytics.tasks.personal_task import calc_all_diseases
from hereditasarbor.apps.analytics.tasks.tree_task import get_data_per_family
from hereditasarbor.apps.users.models import User

if TYPE_CHECKING:
    from hereditasarbor.apps.family.models import FamilyTree
    from hereditasarbor.apps.personals.models import PersonalData


def get_analytic_or_create(user: User) -> tuple[Analytic, bool]:
    """Get or create an analytic for a user.

    Description:
        - If the user has a personal data, check if there is an analytic for that user and create one if it doesn't exist.
        - If the user doesn't have a personal data, check if there is an analytic for that user and create one if it doesn't exist.
        - If the user has a personal data and a tree, check if there is an analytic for that user and create one if it doesn't exist.
        - If the user doesn't have a personal data and a tree, check if there is an analytic for that user and create one if it doesn't exist.
        - If the user has a personal data and a tree, check if there is an analytic for that user and create one if it doesn't exist.

    Args:
        user (User): The user to get or create an analytic for.

    Returns:
        tuple[Analytic, bool]: The analytic and a boolean indicating whether the analytic was created.
    """

    analytic = Analytic.objects.create(user=user)
    created = True

    personal_data: PersonalData = user.get_personal_data()
    personal_analytic = AnalyticPersonal.objects.filter(
        last_change=personal_data.last_update,
    )
    if len(personal_analytic) > 0:
        analytic_personal_data = personal_analytic[0]
        personal_created = False
    else:
        analytic_personal_data = AnalyticPersonal.objects.create(
            last_change=personal_data.last_update,
            analytic=analytic,
        )
        personal_created = True

    tree: FamilyTree = user.get_tree()
    analytic_tree_list = AnalyticTree.objects.filter(
        last_change=tree.last_update,
    )
    if len(analytic_tree_list) > 0:
        analytic_tree = analytic_tree_list[0]
        tree_created = False
    else:
        analytic_tree = AnalyticTree.objects.create(
            last_change=tree.last_update,
            analytic=analytic,
        )
        tree_created = True

    if personal_created and tree_created:
        # analisis totalmente nuevo
        analytic_tree.result = get_data_per_family(
            tree_pk=user.family_tree.pk,
        )
        analytic_personal_data.result = calc_all_diseases(
            personal_data=user.get_personal_data(),
        )

        analytic.save()
        analytic_tree.save()
        analytic_personal_data.save()
        # optener resultados task
    elif not personal_created and tree_created:
        # arbol nuevo & personal antiguo
        # obtener resultados data arbol
        # copiar resultado antiguo personal
        analytic_tree.result = get_data_per_family(
            tree_pk=user.family_tree.pk,
        )
        new_analytic_personal_data = AnalyticPersonal(
            analytic=analytic,
            last_change=personal_data.last_update,
            result=analytic_personal_data.result,
        )
        new_analytic_personal_data.save()
        analytic_tree.save()

    elif personal_created and not tree_created:
        # personal nuevo & arbol antiguo
        # obter resultado data personal
        # copiar resultado antiguo arbol
        analytic_personal_data.result = calc_all_diseases(
            personal_data=user.get_personal_data(),
        )
        new_analytic_tree = AnalyticTree(
            analytic=analytic,
            last_change=tree.last_update,
            result=analytic_tree.result,
        )
        new_analytic_tree.save()
        analytic_personal_data.save()
    else:
        # analisis antiguo
        analytic.delete()
        created = False
        analytic = analytic_personal_data.analytic
    return analytic, created
