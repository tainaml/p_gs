from django.conf.urls import url

from apps.core.views import core as CoreView

urlpatterns = [

    url(r'^related-posts/(?P<instance_id>[0-9]+)/(?P<instance_type>[a-z]+)/(?P<post_type>[a-z]+)/(?P<count>[1-9])/$', CoreView.CoreRelatedPosts.as_view(), name='related-posts'),

]