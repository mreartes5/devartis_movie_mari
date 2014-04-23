from django import forms


class RatingForm(forms.Form):
    value = forms.IntegerField(min_value=1, max_value=10, help_text="Please enter a number between 1 to 10")


class TagForm(forms.Form):
    name = forms.CharField(help_text="Enter a tag for this movie")


class SearchForm(forms.Form):
    title = forms.CharField(min_length=3)
    year_from = forms.IntegerField(min_value=0, required=False)
    year_to = forms.IntegerField(min_value=0, required=False)