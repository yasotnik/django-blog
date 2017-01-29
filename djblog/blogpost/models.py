from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User


class BlogSettings(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=50)

    def __str__(self):
        return "Blog settings"


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    body_preview = models.TextField(default="Preview of post", max_length=200, help_text="Brief overview of post")
    body = models.TextField()
    posted = models.DateTimeField(db_index=True, auto_now_add=True)
    image = models.CharField(max_length=1000)
    category = models.ForeignKey('blogpost.Category')

    def __str__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return 'view_blog_post', None, {'slug': self.slug}


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True, db_index=True)
    slug = models.SlugField(max_length=20, unique=True, db_index=True)

    def __str__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return 'view_blog_category', None, {'slug': self.slug}
