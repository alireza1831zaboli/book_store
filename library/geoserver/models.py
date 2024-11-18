from django.db import models

class GeoImage(models.Model):
    image = models.ImageField(upload_to='images/')
    location = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.location

