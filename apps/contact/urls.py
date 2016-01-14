from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$', views.ContactView.as_view(), name='create'),
    url(r'^save/$', views.ContactSaveViews.as_view(), name='save'),

]