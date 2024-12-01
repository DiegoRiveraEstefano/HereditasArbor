from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from hereditasarbor.apps.users.models import User

from .models import Familiar
from .models import FamilyTree


@receiver(post_save, sender=User)
def create_user_tree(sender, instance, created, **kwargs):
    if created:
        tree = FamilyTree(owner=instance)
        tree.save()


@receiver(post_save, sender=Familiar)
def update_familiar(sender, instance, created, **kwargs):
    familiar: Familiar = instance
    familiar.tree.save()


@receiver(pre_delete, sender=Familiar)
def delete_familiar(sender, instance, **kwargs):
    familiar: Familiar = instance
    familiar.tree.save()
