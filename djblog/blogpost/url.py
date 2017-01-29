from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'blogpost'

urlpatterns = [

    # URL for main page /blogpost
    url(r'^$', views.PostsView.as_view(), name='index'),

    # URL for signup
    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    # Logout
    # url(r'^logout_user/$', views.logout_view, name='logout_user'),

    # URL for posts
    url(r'^post/(?P<slug>[^\.]+)/$', views.PostDetailView.as_view(), name='post'),

    # Logout URL
    url(r'^accounts/', include('registration.backends.simple.urls')),

    url('^', include('django.contrib.auth.urls')),

]