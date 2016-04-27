from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^job/', views.job, name='job'),
    url(r'^', views.do_list, name='list'),
]
