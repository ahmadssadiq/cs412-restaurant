from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from .models import Profile, StatusMessage, Image, Friend
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import UpdateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateProfileForm

class ShowAllProfilesView(ListView):
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                profile = self.request.user.profile  # Check if the user has a profile
                print("User has a profile:", profile)
            except Profile.DoesNotExist:
                print("User does not have a profile")
        else:
            print("User is not authenticated")
        return context


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

class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_creation_form' not in context:
            context['user_creation_form'] = UserCreationForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        user_creation_form = UserCreationForm(request.POST)
        self.object = None

        if form.is_valid() and user_creation_form.is_valid():
            user = user_creation_form.save()
            print(f"Creating user: {user.username}, ID: {user.id}")

            # Check if a profile already exists for this user
            if Profile.objects.filter(user=user).exists():
                # Return with an error message if a profile already exists
                return self.render_to_response(
                    self.get_context_data(
                        form=form,
                        user_creation_form=user_creation_form,
                        error="A profile already exists for this user."
                    )
                )

            # Create a new profile if it doesn't exist
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('show_profile', pk=profile.pk)
        else:
            # Log errors for debugging purposes
            print("Form is not valid")
            print("Profile form errors:", form.errors)
            print("User creation form errors:", user_creation_form.errors)
            
            # Return the form with validation errors
            return self.render_to_response(
                self.get_context_data(form=form, user_creation_form=user_creation_form)
            )


class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"
    login_url = 'login'

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


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"
    login_url = 'login'

    def get_success_url(self):
        return reverse("show_profile", kwargs={"pk": self.object.pk})


class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    context_object_name = "status_message"
    login_url = 'login'

    def get_success_url(self):
        return reverse("show_profile", kwargs={"pk": self.object.profile.pk})


class CreateFriendView(LoginRequiredMixin, View):
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        # Get the two profiles involved in the friendship
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        other_profile = get_object_or_404(Profile, pk=self.kwargs['other_pk'])

        # Check if the profiles are not the same (self-friending is not allowed)
        if profile != other_profile:
            profile.add_friend(other_profile)

        # Redirect to the profile page after adding the friend
        return redirect('show_profile', pk=profile.pk)


class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_object_name = "profile"
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        # Fetching the news feed for the profile
        context['news_feed'] = profile.get_news_feed()
        return context

class FriendSuggestionsView(ListView):
    model = Profile
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = "friend_suggestions"

    def get_queryset(self):
        current_profile = self.request.user.profile
        return Profile.objects.exclude(id=current_profile.id).exclude(
            id__in=[friend.id for friend in current_profile.get_friends()]
        )