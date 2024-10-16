from django.db import models
from django.utils import timezone


class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    image_url = models.URLField(blank=True)  # Optional field for the profile image URL

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class StatusMessage(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.message[:50]}... ({self.timestamp})"
