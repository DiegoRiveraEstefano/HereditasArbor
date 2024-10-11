from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from hereditasarbor.apps.users.models import User

from .models import FamilyTree


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        tree = FamilyTree(owner=instance)
        tree.save()
