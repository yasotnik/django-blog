from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Category
from django import forms


class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        # fields = ['avatar', 'facebook', 'twitter']
        exclude = ['user', 'slug', 'user_group', 'username']


class ProfileAdminForm(forms.ModelForm):

    class Meta:
        model = Profile
        # exclude = ['user', 'slug', 'username']
        fields = ['user_group']


class PostForm(forms.ModelForm):

    # categories = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)

    class Meta:
        model = Post
        exclude = ['author', 'slug']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ['user', 'profile', 'post']


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['title']
