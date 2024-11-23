from celery import shared_task
from .models import Notification, SystemReport
from shop.models import CustomUser, Purchase
from django.utils.timezone import now
from datetime import timedelta


@shared_task
def create_notification(user_id, message):
    try:
        user = CustomUser.objects.get(id=user_id)
        Notification.objects.create(user=user, message=message)
    except CustomUser.DoesNotExist:
        pass


@shared_task
def generate_admin_report():
    users_last_hour = CustomUser.objects.filter(
        date_joined__gte=now() - timedelta(hours=1)
    ).count()
    purchases_last_hour = Purchase.objects.filter(
        purchased_at__gte=now() - timedelta(hours=1)
    ).count()
    returns_last_hour = Purchase.objects.filter(
        is_returned=True, purchased_at__gte=now() - timedelta(hours=1)
    ).count()

    SystemReport.objects.create(
        users_last_hour=users_last_hour,
        purchases_last_hour=purchases_last_hour,
        returns_last_hour=returns_last_hour,
    )
