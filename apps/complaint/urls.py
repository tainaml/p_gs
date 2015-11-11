from django.conf.urls import url
from . import views
from . import views

urlpatterns = [
    url(r'^(?P<complaint>\w{0,50})/$', views.ComplaintView.as_view(), name='report')
]