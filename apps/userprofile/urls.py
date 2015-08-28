from django.conf.urls import url
from . import views

urlpatterns = [

    # url(r'^$', views.index, name='index'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^update_profile/$', views.update_profile, name='update_profile'),
    url(r'^get_state/$', views.get_state, name='get_state'),
    url(r'^get_city/$', views.get_city, name='get_city'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/$', views.show, name='show'),

]