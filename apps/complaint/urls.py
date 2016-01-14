from django.conf.urls import url

from . import views

urlpatterns = [

    # url(r'^(?P<complaint>\w{0,50})/$', views.ComplaintView.as_view(), name='report')
    url(r'^(?P<object_type>[a-z]+)/(?P<object_id>[0-9]+)$', views.ComplaintView.as_view(), name='report')

]