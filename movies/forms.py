from django import forms

from movies.models import UserProfile, MyUser
from movies.models import Movie


class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Please enter a username.")
    email = forms.CharField(help_text="Please enter your email.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter a password.")

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password']


class UserProfileForm(forms.ModelForm):
    website = forms.URLField(help_text="Please enter your website.", required=False)
    picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)

    class Meta:
        model = UserProfile
        fields = ['website', 'picture']


class RatingForm(forms.ModelForm):
    value = forms.IntegerField(help_text="Please enter a number between 1 to 10.")

    class Meta:
        model = Movie
        fields = ['value']


class UserWatchlistForm(forms.ModelForm):
    class Meta:
        model = MyUser