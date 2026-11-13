from django.db import models

from .tasks import decrypt_data
from .tasks import encrypt_data


class EncryptUserDataFieldCustom(models.TextField):
    """
    a custom field that encrypt the data
    """

    description = "a field that encrypt the data"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value, instance=None):
        """
        make the pre preparations for db inserts/update
        """
        user_pk = getattr(instance, self.user.pk)
        return encrypt_data(value, user_pk=user_pk)

    def from_db_value(self, value, expression, connection, context):
        """
        make the preparations for db reads
        """
        instance = context.get("instance")
        user_pk = getattr(instance, self.user.pk)
        return decrypt_data(value, user_pk=user_pk)
