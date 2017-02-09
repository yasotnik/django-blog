from django.contrib.auth.models import User
from .models import Profile, Post
from django import forms


class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['avatar', 'facebook', 'twitter']


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ['author', 'slug']
