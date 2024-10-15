from django.views.generic import ListView, DetailView
from .models import Profile


# View to show all profiles
class ShowAllProfilesView(ListView):
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"


# View to show a single profile's page
class ShowProfilePageView(DetailView):
    model = Profile
    template_name = "mini_fb/show_profile.html"
