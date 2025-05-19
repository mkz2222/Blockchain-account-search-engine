from django.urls import include, path
from django.urls import re_path
from . import views


urlpatterns = [
#/user/username
    # re_path(r'^(?P<user_name>[0-z]+|[0-z.]+)$', views.user_view, name='user'),
    path('myaccount', views.user_account, name='user_account'),
    path('mycontent', views.user_act, name='user_act'),
    path('setting', views.user_setting, name='user_setting'),
]