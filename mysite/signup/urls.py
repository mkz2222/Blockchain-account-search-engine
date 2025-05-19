from django.urls import include, path
from django.urls import re_path
from . import views

urlpatterns = [
#/signup/
    re_path(r'^$', views.signup, name='signup'),
]
