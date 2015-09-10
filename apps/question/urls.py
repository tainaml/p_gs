from django.conf.urls import url
from . import views

urlpatterns = [

    #url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create_question, name='create'),
    url(r'^save/$', views.save_question, name='save'),
    url(r'^edit/(?P<question_id>[0-9]+)$', views.edit_question, name='edit'),
    url(r'^update/$', views.update_question, name='update'),
    url(r'^show/(?P<question_id>[0-9]+)$', views.show_question, name='show'),
    url(r'^comment_reply/$', views.comment_reply, name='comment_reply'),
    url(r'^update_reply/$', views.update_reply, name='update_reply'),

    ]