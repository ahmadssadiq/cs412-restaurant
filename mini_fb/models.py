from django.db import models


class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    image_url = models.URLField(blank=True)  # Optional field for the profile image URL

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
