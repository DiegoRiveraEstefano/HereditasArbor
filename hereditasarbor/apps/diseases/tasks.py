from celery import shared_task

from hereditasarbor.apps.diseases.models import Disease


@shared_task()
def get_disaes_count():
    """A pointless Celery task to demonstrate usage."""
    return Disease.objects.count()
