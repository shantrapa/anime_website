from .models import *
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AnimeshnikForm(ModelForm):
    class Meta:
        model = Animeshnik
        fields = "__all__"
        exclude = ['user']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AnimeSearchForm(forms.Form):
    title = forms.CharField(label='Название аниме', max_length=100)

class AnimeForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required = True
    )

    class Meta:
        model = Anime
        fields = "__all__"
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'})
        }