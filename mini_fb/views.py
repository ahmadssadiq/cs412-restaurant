from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, StatusMessage
from .forms import CreateProfileForm, CreateStatusMessageForm


# Existing views
class ShowAllProfilesView(ListView):
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = "mini_fb/show_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_messages"] = StatusMessage.objects.filter(profile=self.object)
        return context


# New view for creating a profile
class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def get_success_url(self):
        return reverse("show_profile", kwargs={"pk": self.object.pk})


# status message
class CreateStatusMessageView(CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def form_valid(self, form):
        # Attach the Profile object to the status message before saving
        profile = Profile.objects.get(pk=self.kwargs["pk"])
        form.instance.profile = profile
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the profile to the context
        context["profile"] = Profile.objects.get(pk=self.kwargs["pk"])
        return context

    def get_success_url(self):
        # After posting a status, redirect to the profile page
        return reverse("show_profile", kwargs={"pk": self.kwargs["pk"]})
