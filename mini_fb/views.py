from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, DetailView
from .models import Profile, StatusMessage, Profile
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import UpdateView
from django.views import View


# Existing views
class ShowAllProfilesView(ListView):
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetching the friends of the current profile
        profile = self.get_object()
        # Example of obtaining friend suggestions (you may refine this logic)
        context['friend_suggestions'] = Profile.objects.exclude(
            pk__in=[friend.pk for friend in profile.get_friends()]
        ).exclude(pk=profile.pk)
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
        # Save the status message
        sm = form.save(commit=False)

        # Attach the Profile object to the status message before saving
        sm.profile = Profile.objects.get(pk=self.kwargs["pk"])
        sm.save()

        # Handle image files
        files = self.request.FILES.getlist("files")
        for file in files:
            Image.objects.create(image_file=file, status_message=sm)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the profile to the context
        context["profile"] = Profile.objects.get(pk=self.kwargs["pk"])
        return context

    def get_success_url(self):
        # After posting a status, redirect to the profile page
        return reverse("show_profile", kwargs={"pk": self.kwargs["pk"]})


class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    def get_success_url(self):
        return reverse("show_profile", kwargs={"pk": self.object.pk})


class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    context_object_name = "status_message"

    def get_success_url(self):
        return reverse("show_profile", kwargs={"pk": self.object.profile.pk})

class CreateFriendView(View):
    def dispatch(self, request, *args, **kwargs):
        # Get the two profiles involved in the friendship
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        other_profile = get_object_or_404(Profile, pk=self.kwargs['other_pk'])

        # Check if the profiles are not the same (self-friending is not allowed)
        if profile != other_profile:
            profile.add_friend(other_profile)

        # Redirect to the profile page after adding the friend
        return redirect('show_profile', pk=profile.pk)

class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = "mini_fb/news_feed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_feed'] = self.object.get_news_feed()
        return context
