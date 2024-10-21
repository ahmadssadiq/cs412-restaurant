from django import forms
from .models import Profile, StatusMessage


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "city", "email", "image_url"]


class CreateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ["message"]

    def form_valid(self, form):
        form.instance.profile = Profile.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["birth_date", "city", "email", "bio"]
