from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from hereditasarbor.apps.users.models import User

from .models import Familiar
from .models import FamilyTree


@receiver(post_save, sender=User)
def on_user_create_create_family_tree(sender, instance, created, **kwargs):
    """Create a family tree when a user is created.

    Args:
        sender (User): The sender of the signal.
        instance (User): The instance of the signal.
        created (bool): Whether the instance is created.
        **kwargs: Additional keyword arguments.
    """
    if created:
        tree = FamilyTree(owner=instance)
        tree.save()


@receiver(post_save, sender=Familiar)
def on_update_familiar(sender, instance, created, **kwargs):
    """Update the family tree when a familiar is created or updated.

    Args:
        sender (Familiar): The sender of the signal.
        instance (Familiar): The instance of the signal.
        created (bool): Whether the instance is created.
        **kwargs: Additional keyword arguments.
    """
    familiar: Familiar = instance
    familiar.tree.save()


@receiver(pre_delete, sender=Familiar)
def on_delete_familiar(sender, instance, **kwargs):
    """Delete the family tree when a familiar is deleted.

    Args:
        sender (Familiar): The sender of the signal.
        instance (Familiar): The instance of the signal.
        **kwargs: Additional keyword arguments.
    """
    familiar: Familiar = instance
    familiar.tree.save()
