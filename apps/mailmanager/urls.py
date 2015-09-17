from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^test/$', views.test_async, name='test_async'),
    url('^send/', views.send_async, name='send_async')
]