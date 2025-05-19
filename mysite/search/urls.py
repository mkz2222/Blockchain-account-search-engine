from django.urls import include, path
from django.urls import re_path
from . import views

urlpatterns = [
#/search/
    re_path(r'^$', views.hello, name='search'),
]
