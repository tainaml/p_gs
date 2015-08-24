__author__ = 'phillip'
from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^signup/', views.signup, name='signup'),
    url(r'^register/', views.register, name='register'),
    url(r'^signup_without_captcha/', views.signup_without_captcha, name='signup_without_captcha'),

]