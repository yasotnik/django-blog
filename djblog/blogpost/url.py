from django.conf.urls import url
from . import views

app_name = 'blogpost'

urlpatterns = [

    # URL for main page /blog
    url(r'^$', views.home_page, name='home'),

]