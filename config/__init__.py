# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery_app import app as celery_app

__all__ = ("celery_app",)

from django.template.defaulttags import register

@register.filter(name='split')
def split(value, key): 
 
    value.split("key")
    return value.split(key)