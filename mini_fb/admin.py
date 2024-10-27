from django.contrib import admin
from .models import Profile, Friend  # Import Friend model as well

admin.site.register(Profile)

@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ('profile1', 'profile2', 'timestamp') 