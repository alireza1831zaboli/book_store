from django.urls import path
from .views import NotificationListView, NotificationPageView

urlpatterns = [
    path(
        "notification-list/", NotificationListView.as_view(), name="notification-list"
    ),
]
