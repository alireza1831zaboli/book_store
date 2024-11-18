from celery import shared_task
from .models import Notifications

@shared_task
def create_notification(user_id, message):
    Notifications.objects.create(user_id=user_id, message=message)