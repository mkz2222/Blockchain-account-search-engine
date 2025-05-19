"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.views.generic.base import RedirectView
from signup import views as signup_views
from ajax import views as ajax_views
from user import views as user_views
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('', RedirectView.as_view(url='search/')),


    path('m4d2fg657433sa/', admin.site.urls),
    path('search/', include('search.urls')),
    path('account/', include('acct.urls')),
    path('group/', include('group.urls')),


    path('login/', signup_views.user_login, name='login'),
    path('signin/', signup_views.user_signin, name='signin'),
    path('logout/', signup_views.user_logout, name='logout'),

    path('signup/', include('signup.urls')),
    
    path('contact/', signup_views.contact, name='contact'),


    path('activation/', signup_views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', signup_views.activate, name='activate'),

    path('user_agreement/', signup_views.agreement, name='agreement'),
    path('user_privacy/', signup_views.privacy, name='privacy'),
    path('advertise/', signup_views.advertise, name='advertise'),
    path('test/', signup_views.test, name='test'),


    path('user/', include('user.urls')),

    path('s1', ajax_views.change_email, name='change_email'),
    path('s2', ajax_views.change_password, name='change_password'),
    path('s3', ajax_views.check_username, name='check_username'),
    path('s4', ajax_views.check_email, name='check_email'),
    path('s5', ajax_views.reset_pass, name='reset_pass'),
    path('s6', ajax_views.signup, name='ajax_signup'),
    path('s7', ajax_views.comment, name='ajax_comment'),
    path('s8', ajax_views.like, name='ajax_like'),
    path('s9', ajax_views.reply, name='ajax_reply'),
    path('a1', ajax_views.delete, name='ajax_delete'),
    path('a2', ajax_views.contact, name='ajax_contact'),
    path('a3', ajax_views.resend_link, name='ajax_resend_link'),




    path('emailupdate/<uidb64>/<token>/', user_views.update_email, name='update_email'),
    path('passwordreset/', user_views.forgot_password, name='forgot_password'),
    path('reset_password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='reset_password'),
    path('reset_password/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),



    # path('test/', include('test01.urls')),
    # path('test02/', include('test02.urls')),


]