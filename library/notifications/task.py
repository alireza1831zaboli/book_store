from celery import shared_task
from .models import Notification
from shop.models import CustomUser


@shared_task
def create_notification(user_id, message):
    try:
        user = CustomUser.objects.get(id=user_id)
        Notification.objects.create(user=user, message=message)
    except CustomUser.DoesNotExist:
        pass
