from django.urls import include, path
from django.urls import re_path
from . import views


urlpatterns = [
#/account/groupname
    re_path(r'^(?P<group_name>[0-z]+)$', views.group, name='group'),
]