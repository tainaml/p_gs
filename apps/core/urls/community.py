from django.conf.urls import url
from ..views.community import views, CoreCommunityView, CoreCommunityFollowersView

view_community_show = CoreCommunityView.as_view()
view_community_followers = CoreCommunityFollowersView.as_view()

urlpatterns = [
    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)$', view_community_show, name='show'),
    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followers/$', view_community_followers, name='get_followers'),
    ]