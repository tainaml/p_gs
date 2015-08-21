__author__ = 'phillip'

from django.conf.urls import url

import views

urlpatterns = [
    url(r'^sign-up/$', views.sign_up, name='signup'),
    url(r'^register/$', views.register, name='register'),
    ]