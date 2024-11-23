from django.db import models
from shop.models import CustomUser
from django.utils.timezone import now


class Notification(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.TextField()
    created_at = models.DateTimeField(default=now)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:30]}"


class SystemReport(models.Model):
    created_at = models.DateTimeField(default=now)
    users_last_hour = models.IntegerField(default=0)
    purchases_last_hour = models.IntegerField(default=0)
    returns_last_hour = models.IntegerField(default=0)
