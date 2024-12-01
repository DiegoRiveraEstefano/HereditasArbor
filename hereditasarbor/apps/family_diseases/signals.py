from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import FamiliarDiseases


@receiver(post_save, sender=FamiliarDiseases)
def update_tree(sender, instance, created, **kwargs):
    familiar_disease: FamiliarDiseases = instance
    familiar_disease.familiar.tree.save()


@receiver(pre_delete, sender=FamiliarDiseases)
def pre_delete_disease(sender, instance, **kwargs):
    familiar_disease: FamiliarDiseases = instance
    familiar_disease.familiar.tree.save()
