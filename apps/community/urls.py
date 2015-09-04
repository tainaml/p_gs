from django.conf.urls import url
from . import views

view_community_show = views.CommunityView.as_view()


urlpatterns = [
    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)$', view_community_show, name='show'),
]