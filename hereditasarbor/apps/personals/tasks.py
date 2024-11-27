from cryptography.fernet import Fernet
from django.conf import settings
from celery import shared_task
from functools import lru_cache
from hereditasarbor.apps.users.models import User

@shared_task
@lru_cache(maxsize=128)
def encrypt_data(raw_data: str, user_pk: int) -> str:
    fernet = Fernet("-".join([settings.SECRET_KEY, str(user_pk)]))
    return fernet.encrypt(raw_data)


@shared_task
@lru_cache(maxsize=128)
def decrypt_data(encrypted_data: str, user_pk: int) -> str:
    fernet = Fernet("-".join([settings.SECRET_KEY, str(user_pk)]))
    return fernet.decrypt(encrypted_data)
