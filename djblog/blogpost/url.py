from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'blogpost'

urlpatterns = [

    # URL for main page /blogpost
    url(r'^$', views.PostsView.as_view(), name='index'),

    # URL for signup
    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    # URL for posts
    url(r'^post/(?P<slug>[^\.]+)/$', views.PostDetailView.as_view(), name='post'),

    # URL for creating a post
    url(r'add_post/$', views.AddPostView.as_view(), name='add_post'),

    # Login
    url(r'^login/$', views.LoginView.as_view(), name='login_user'),

    # Logout
    url(r'^logout_user/$', views.LogoutView.as_view(), name='logout_user'),

    # Profile settings
    url(r'^profile/$', views.ProfileUpdate.as_view(), name='profile_edit'),

    # Profile
    url(r'^user/(?P<slug>[^\.]+)/$', views.ProfileView.as_view(), name='profile'),

    # URL for posts
    url(r'^category/(?P<slug>[^\.]+)/$', views.CategoryDetailView.as_view(), name='category_view'),

    # URL for posts
    url(r'^post/(?P<slug>[^\.]+)/delete_comment/(?P<pk>[0-9]+)$', views.CommentDelete.as_view(), name='comment_delete'),

]
