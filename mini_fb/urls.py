from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView, CreateProfileView

urlpatterns = [
    # URL for showing all profiles
    path("", ShowAllProfilesView.as_view(), name="show_all_profiles"),
    # URL for showing a specific profile by primary key
    path("profile/<int:pk>/", ShowProfilePageView.as_view(), name="show_profile"),
    # URL for creating a new profile
    path("create_profile/", CreateProfileView.as_view(), name="create_profile"),
]
