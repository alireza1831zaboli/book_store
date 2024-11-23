from django.urls import path
from .views import NotificationListView, AdminReportView

urlpatterns = [
    path(
        "notification-list/", NotificationListView.as_view(), name="notification-list"
    ),
    path("admin-report/", AdminReportView.as_view(), name="admin-report"),
]
