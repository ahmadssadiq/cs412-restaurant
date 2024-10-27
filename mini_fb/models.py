from django.db import models
from django.utils import timezone


class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    image_url = models.URLField(blank=True)

    def get_friends(self):
        friends_1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        friends_2 = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)
        friend_ids = set(friends_1).union(set(friends_2))
        return Profile.objects.filter(id__in=friend_ids)

    def add_friend(self, other):
        if self == other:
            return 

        if not Friend.objects.filter(profile1=self, profile2=other).exists() and not Friend.objects.filter(profile1=other, profile2=self).exists():
            Friend.objects.create(profile1=self, profile2=other)
    
     def get_news_feed(self):
        friends = self.get_friends()
        return StatusMessage.objects.filter(profile__in=friends).order_by('-timestamp')


    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class StatusMessage(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.message[:50]}... ({self.timestamp})"

    def get_images(self):
        return Image.objects.filter(status_message=self)


class Image(models.Model):
    image_file = models.ImageField(upload_to="images/")
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Image {self.id} for {self.status_message}"


class Friend(models.Model):
    profile1 = models.ForeignKey('Profile', related_name="profile1", on_delete=models.CASCADE)
    profile2 = models.ForeignKey('Profile', related_name="profile2", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}"