__author__ = 'phillip'

from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^act/(?P<object_to_link>[0-9]+)/(?P<content>[a-zA-Z]+)/(?P<action>[a-zA-Z]+)', views.act, name='act')
]