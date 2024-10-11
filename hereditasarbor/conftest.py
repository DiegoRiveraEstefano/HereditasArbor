import pytest

from hereditasarbor.apps.diseases.models import Disease
from hereditasarbor.apps.diseases.models import DiseaseCategory
from hereditasarbor.apps.diseases.tests.factories import DisaesCategoryFactory
from hereditasarbor.apps.diseases.tests.factories import DisaesFactory
from hereditasarbor.apps.users.models import User
from hereditasarbor.apps.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()


@pytest.fixture
def disease_category(db) -> DiseaseCategory:
    return DisaesCategoryFactory()


@pytest.fixture
def disease(db) -> Disease:
    return DisaesFactory()
