from hereditasarbor.apps.analytics.models import Analytic
from hereditasarbor.apps.analytics.models import AnalyticPersonal
from hereditasarbor.apps.analytics.models import AnalyticTree
from hereditasarbor.apps.analytics.tasks.personal_task import calc_all_diseases
from hereditasarbor.apps.analytics.tasks.tree_task import get_data_per_family
from hereditasarbor.apps.family.models import FamilyTree
from hereditasarbor.apps.personals.models import PersonalData
from hereditasarbor.apps.users.models import User


def get_analytic_or_create(user: User) -> tuple[Analytic, bool]:
    analytic = Analytic.objects.create(user=user)
    created = True

    personal_data: PersonalData = user.get_personal_data()
    analytic_personal_data, personal_created = AnalyticPersonal.objects.get_or_create(
        last_change=personal_data.last_update,
        defaults={"analytic": analytic},
    )

    tree: FamilyTree = user.get_tree()
    analytic_tree, tree_created = AnalyticTree.objects.get_or_create(
        last_change=tree.last_update,
        defaults={"analytic": analytic},
    )

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
        analytic_tree.save()
    else:
        # analisis antiguo
        analytic.delete()
        created = False
        analytic = analytic_personal_data.analytic

    return analytic, created
