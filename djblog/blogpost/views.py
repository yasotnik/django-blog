from django.shortcuts import render
from django.views import generic
from .models import Post, Category


class PostsView(generic.ListView):
    template_name = 'blogpost/index.html'

    def get_queryset(self):
        return Post.objects.all()


class PostView(generic.DeleteView):
    model = Post
    template_name = 'blogpost/post.html'