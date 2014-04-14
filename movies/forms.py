from django import forms

from movies.models import UserProfile, MyUser
from movies.models import Movie, Tag


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


class RatingForm(forms.Form):
    value = forms.IntegerField(min_value=1, max_value=10, help_text="Please enter a number between 1 to 10.")


class TagForm(forms.Form):
    name = forms.CharField(help_text="Enter a tag for this movie")



class SearchForm(forms.ModelForm):
    title = forms.CharField(help_text="Enter the movie's title")
    year_from = forms.IntegerField(help_text="Enter year from")
    year_to = forms.IntegerField(help_text="Enter year to")

    class Meta:
        model = Movie
        fields = ['title', 'year_from', 'year_to']