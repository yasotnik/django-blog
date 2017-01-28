from django.conf.urls import url
from . import views

app_name = 'blogpost'

urlpatterns = [

    # URL for main page /blogpost
    url(r'^$', views.PostsView.as_view(), name='index'),

    # URL for posts
    url(r'^view/(?P<slug>[^\.]+)/$', views.PostDetailView.as_view(), name='post'),

]