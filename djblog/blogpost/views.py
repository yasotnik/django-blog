from django.shortcuts import render
from django.views import generic
from .models import Post, Category, BlogSettings


class PostsView(generic.ListView):
    template_name = 'blogpost/index.html'

    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PostsView, self).get_context_data(**kwargs)
        context['blog'] = BlogSettings.objects.all()[0]
        return context

    # def get_queryset(self):
    #     return Post.objects.all()


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blogpost/post.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['blog'] = BlogSettings.objects.all()[0]
        return context
