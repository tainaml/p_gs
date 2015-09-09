from django.conf.urls import url
from . import views

urlpatterns = [

    #url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create_question, name='create'),
    url(r'^save/$', views.save_question, name='save'),
    url(r'^edit/(?P<question_id>[0-9]+)$', views.edit_question, name='edit'),
    url(r'^update/$', views.update_question, name='update'),

    ]