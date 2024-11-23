from rest_framework import serializers
from .models import Notification, SystemReport


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "message", "created_at", "read"]


class SystemReportSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = SystemReport
        fields = [
            "users_last_hour",
            "purchases_last_hour",
            "returns_last_hour",
            "created_at",
        ]
