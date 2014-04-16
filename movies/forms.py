from django import forms
from movies.models import UserProfile, MyUser


class UserForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password']


class UserProfileForm(forms.ModelForm):
    website = forms.URLField(required=False)
    picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ['website', 'picture']


class RatingForm(forms.Form):
    value = forms.IntegerField(min_value=1, max_value=10, help_text="Please enter a number between 1 to 10")


class TagForm(forms.Form):
    name = forms.CharField(help_text="Enter a tag for this movie")


class SearchForm(forms.Form):
    title = forms.CharField(min_length=3)
    year_from = forms.IntegerField(min_value=0, required=False)
    year_to = forms.IntegerField(min_value=0, required=False)