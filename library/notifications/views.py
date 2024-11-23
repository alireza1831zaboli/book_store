from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Notification, SystemReport
from .serializers import NotificationSerializer, SystemReportSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from .task import generate_admin_report


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user).order_by(
            "-created_at"
        )
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_notifications = paginator.paginate_queryset(notifications, request)
        serializer = NotificationSerializer(paginated_notifications, many=True)

        Notification.objects.filter(
            id__in=[notification.id for notification in paginated_notifications]
        ).update(read=True)

        return paginator.get_paginated_response(serializer.data)


class AdminReportView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        generate_admin_report.delay()
        latest_report = SystemReport.objects.order_by("-created_at").first()

        serializer = SystemReportSerializer(latest_report)
        return Response(serializer.data, status=status.HTTP_200_OK)
