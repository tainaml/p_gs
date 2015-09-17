from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)$', views.CommunityView.as_view(), name='show'),
]