from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify


class BlogSettings(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=50)

    def __str__(self):
        return "Blog settings"


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    FOLLOWER = 'FL'
    WRITER = 'WR'
    USER_GROUP = (
        (FOLLOWER, 'Follower'),
        (WRITER, 'Writer'),
    )
    user_group = models.CharField(max_length=2, choices=USER_GROUP, default=FOLLOWER)
    slug = models.SlugField(max_length=20, db_index=True)
    avatar = models.CharField(max_length=200)
    facebook = models.CharField(max_length=30, blank=True)
    twitter = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username

    def get_username(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def save(self, *args, **kwargs):
            self.slug = slugify(self.user.username)
            super(Profile, self).save(*args, **kwargs)