from rest_framework.response import Response
from .models import Notifications

def get_notifications(request):
    notifications = Notifications.objects.filter(user=request.user, is_read=False)
    data = [{'id': n.id, 'message': n.message, 'created_at': n.created_at} for n in notifications]
    return Response({'notifications': data})

def mark_as_read(request, notification_id):
    notification = Notifications.objects.get(id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return Response({'message': 'Notification marked as read.'})