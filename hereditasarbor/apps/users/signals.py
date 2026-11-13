from django.db.models.signals import post_save
from django.dispatch import receiver

from hereditasarbor.apps.users.models import User


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """hash the password of the user

    Args:
        sender (User): Model User
        instance (User): the User
        created (bool): if the user has be created
    """
    if created:
        user: User = instance
        raw_password: str = user.password
        user.set_password(raw_password=raw_password)
        user.save(update_fields=["password"])
        user.check_password(raw_password=raw_password)
