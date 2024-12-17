from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import FamiliarDiseases


@receiver(post_save, sender=FamiliarDiseases)
def on_create_family_disease_update_tree(sender, instance, created, **kwargs):
    """Update the family tree when a family disease is created or updated.

    Args:
        sender (FamiliarDiseases): The sender of the signal.
        instance (FamiliarDiseases): The instance of the signal.
        created (bool): Whether the instance is created.
        **kwargs: Additional keyword arguments.
    """
    familiar_disease: FamiliarDiseases = instance
    familiar_disease.familiar.tree.save()


@receiver(pre_delete, sender=FamiliarDiseases)
def on_pre_delete_disease_update_tree(sender, instance, **kwargs):
    """Update the family tree when a family disease is deleted.

    Args:
        sender (FamiliarDiseases): The sender of the signal.
        instance (FamiliarDiseases): The instance of the signal.
        **kwargs: Additional keyword arguments.
    """
    familiar_disease: FamiliarDiseases = instance
    familiar_disease.familiar.tree.save()
