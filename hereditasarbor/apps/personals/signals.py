from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import PersonalTimeStampData


@receiver(post_save, sender=PersonalTimeStampData)
def on_update_personal_data(sender, instance, created, **kwargs):
    """Update the personal data when a personal time stamp data is created or updated.

    Args:
        sender (PersonalTimeStampData): The sender of the signal.
        instance (PersonalTimeStampData): The instance of the signal.
        created (bool): Whether the instance is created.
        **kwargs: Additional keyword arguments.
    """

    time_stamp: PersonalTimeStampData = instance
    time_stamp.personal_data.save()
