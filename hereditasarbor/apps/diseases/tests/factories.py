import random
from collections.abc import Sequence
from typing import Any

from factory import Faker
from factory import SubFactory
from factory import post_generation
from factory.django import DjangoModelFactory
from faker.providers import lorem

from hereditasarbor.apps.diseases.models import Disease
from hereditasarbor.apps.diseases.models import DiseaseCategory
from hereditasarbor.apps.users.models import User


class DisaesCategoryFactory(DjangoModelFactory[DiseaseCategory]):
    name = Faker("sentence", n_words=2)
    description = Faker("sentence", n_words=2)

    class Meta:
        model = DiseaseCategory
        django_get_or_create = ["name"]


class DisaesFactory(DjangoModelFactory[Disease]):
    name = Faker("sentence", n_words=2)
    description = Faker("sentence", n_words=2)
    endogena = bool(random.choices([0, 1]))
    chance = random.random()
    category = SubFactory(DisaesCategoryFactory)

    """@post_generation"""

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        """Save again the instance if creating and at least one hook ran."""
        if create and results and not cls._meta.skip_postgeneration_save:
            # Some post-generation hooks ran, and may have modified us.
            instance.save()

    class Meta:
        model = Disease
        django_get_or_create = ["name"]
