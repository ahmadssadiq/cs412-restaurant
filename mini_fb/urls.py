from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import (
    ShowAllProfilesView,
    ShowProfilePageView,
    CreateProfileView,
    CreateStatusMessageView,
    UpdateProfileView,
    DeleteStatusMessageView,
    CreateFriendView,
    ShowNewsFeedView,
    FriendSuggestionsView
)

urlpatterns = [
    # URL for showing all profiles
    path("", ShowAllProfilesView.as_view(), name="show_all_profiles"),
    # URL for showing a specific profile by primary key
    path("profile/<int:pk>/", ShowProfilePageView.as_view(), name="show_profile"),
    # URL for creating a new profile
    path("create_profile/", CreateProfileView.as_view(), name="create_profile"),
    # URL for creating a new status message
    path("profile/<int:pk>/create_status/", CreateStatusMessageView.as_view(), name="create_status"),
    # URL for updating a profile
    path("profile/<int:pk>/update/", UpdateProfileView.as_view(), name="update_profile"),
    # URL for deleting a status message
    path("status/<int:pk>/delete/", DeleteStatusMessageView.as_view(), name="delete_status"),
    # URL for adding a friend
    path("profile/<int:pk>/add_friend/<int:other_pk>/", CreateFriendView.as_view(), name="add_friend"),
    # URL for showing a user's news feed
    path("profile/<int:pk>/news_feed/", ShowNewsFeedView.as_view(), name="news_feed"),
    # URL for friend suggestions
    path("profile/<int:pk>/friend_suggestions/", FriendSuggestionsView.as_view(), name="friend_suggestions"),
    # URLs for login and logout
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all_profiles'), name='logout'),
]