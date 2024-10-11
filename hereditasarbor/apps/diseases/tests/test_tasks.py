import pytest
from celery.result import EagerResult

from hereditasarbor.apps.diseases.models import Disease
from hereditasarbor.apps.diseases.models import DiseaseCategory
from hereditasarbor.apps.diseases.tasks import get_disaes_count
from hereditasarbor.apps.diseases.tests.factories import DisaesCategoryFactory
from hereditasarbor.apps.diseases.tests.factories import DisaesFactory

pytestmark = pytest.mark.django_db


def test_diseases_count(settings):
    """A basic test to execute the get_users_count Celery task."""
    batch_size = 3
    DisaesFactory.create_batch(batch_size)
    settings.CELERY_TASK_ALWAYS_EAGER = True
    task_result = get_disaes_count.delay()
    assert isinstance(task_result, EagerResult)
    assert task_result.result == batch_size
