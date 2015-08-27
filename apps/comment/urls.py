from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^save/$', views.save, name='save'),
    url(r'^index_teste/$', views.index_teste, name='index_teste'),
]