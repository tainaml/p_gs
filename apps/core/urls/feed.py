from django.conf.urls import url
from ..views import feed as view

urlpatterns = [

    url(r'^set-official/(?P<content_type>[a-z]+)/(?P<object_id>[0-9]+)$', view.FeedContentOfficial.as_view(), name='set-content-official'),

]