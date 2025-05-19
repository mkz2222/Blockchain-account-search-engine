from django.urls import include, path
from django.urls import re_path
from . import views


urlpatterns = [
#/account/accountname
    re_path(r'^(?P<acct_name>[0-z]+|[0-z.]+)$', views.acct, name='acct'),
]
