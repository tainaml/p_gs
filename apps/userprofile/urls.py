from django.conf.urls import url
from . import views

urlpatterns = [

    # url(r'^$', views.index, name='index'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^update_profile/$', views.update_profile, name='update_profile'),
    url(r'^get_state/$', views.get_state, name='get_state'),
    url(r'^get_city/$', views.get_city, name='get_city'),
    url(r'^occupation/$', views.occupation_manage, name='occupation_manage'),
    url(r'^occupation/(?P<occupation_id>[0-9]+)$', views.occupation_show, name='occupation_show'),
    url(r'^occupation/add/$', views.occupation_add, name='occupation_add'),
    url(r'^occupation/create/$', views.occupation_create, name='occupation_create'),
    url(r'^occupation/edit/(?P<occupation_id>[0-9]+)$', views.occupation_edit, name='occupation_edit'),
    url(r'^occupation/update/$', views.occupation_update, name='occupation_update'),
    url(r'^occupation/delete/(?P<occupation_id>[0-9]+)$', views.occupation_delete, name='occupation_delete'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/$', views.show, name='show'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followings/$', views.profile_followings, name='followings'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followers/$', views.profile_followers, name='followers'),

]