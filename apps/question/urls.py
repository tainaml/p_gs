from django.conf.urls import url
from . import views

urlpatterns = [

    #url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create_question, name='create'),
    url(r'^save/$', views.save_question, name='save'),
    #url(r'^edit/$', views.comment, name='comment'),

    ]