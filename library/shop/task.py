from celery import shared_task
from django.utils.timezone import now, timedelta
from django.core.mail import send_mail
from .models import CustomUser, Purchase

@shared_task
def send_admin_report():
    last_hour = now() - timedelta(hours=1)
    new_users = CustomUser.objects.filter(date_joined__gte=last_hour).count()
    new_purchases = Purchase.objects.filter(purchased_at__gte=last_hour).count()
    returned_books = Purchase.objects.filter(is_returned=True, purchased_at__gte=last_hour).count()

    message = f"""
    Admin Report:
    - New users: {new_users}
    - New purchases: {new_purchases}
    - Returned books: {returned_books}
    """
    send_mail('Hourly Admin Report', message, 'admin@example.com', ['admin@example.com'])


