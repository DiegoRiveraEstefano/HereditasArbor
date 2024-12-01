from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import PersonalTimeStampData


@receiver(post_save, sender=PersonalTimeStampData)
def update_personal_data(sender, instance, created, **kwargs):
    time_stamp: PersonalTimeStampData = instance
    time_stamp.personal_data.save()
