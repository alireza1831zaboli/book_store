from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.gis.db import models as geomodels
from django.utils.timezone import now, timedelta


class Book(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    avalible = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    owned_books = models.ManyToManyField(Book, related_name="owners", blank=True)
    location = geomodels.PointField(null=True, blank=True)

    def __str__(self):
        return self.username


class Purchase(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(default=now)
    is_returned = models.BooleanField(default=False)

    def can_be_returned(self):
        return now() <= self.purchased_at + timedelta(hours=1)
