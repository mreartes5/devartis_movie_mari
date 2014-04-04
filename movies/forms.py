from django import forms
from django.contrib.auth.models import User

from movies.models import UserProfile
from movies.models import Rating


class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Please enter a username.")
    email = forms.CharField(help_text="Please enter your email.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter a password.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserProfileForm(forms.ModelForm):
    website = forms.URLField(help_text="Please enter your website.", required=False)
    picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)

    class Meta:
        model = UserProfile
        fields = ['website', 'picture']


class RatingForm(forms.ModelForm):
    # value = forms.CharField(max_length=2, help_text="Please enter the points.")
    value = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Rating
        fields = ['value']