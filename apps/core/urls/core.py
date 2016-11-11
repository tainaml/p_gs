from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from apps.core.views import core as CoreView
from apps.core.views import responsibility
from apps.core.views import videos


urlpatterns = [

    # Translators: URL de posts relacionados
    url(_(r'^related-posts/(?P<instance_id>[0-9]+)/(?P<instance_type>[a-z]+)/(?P<post_type>[a-z]+)/(?P<count>[1-9])/$'), CoreView.CoreRelatedPosts.as_view(), name='related-posts'),

    url(_(r'^responsibilities/$'), responsibility.ResponsibilityListView.as_view(), name='responsibilities-list'),

    url(_(r'^responsibilities/(?P<slug>[aA-zZ0-9-_]+)/$'), responsibility.ResponsibilityView.as_view(), name='responsibility'),

    # Translators: URL de videos
    url(_(r'videos/$'), videos.VideoView.as_view(), name='videos-list'),

    # Translators: URL de sobre
    url(_(r'^about/'), CoreView.About.as_view(), name='about'),


    # Translators: URL de sobre
    url(_(r'^rules/'), CoreView.Rules.as_view(), name='rules'),

    # Translators: URL de sobre
    url(_(r'^politica-de-privacidade/'), CoreView.Privacy.as_view(), name='privacy'),


    url(_(r'^oembed/'), CoreView.OEmbed.as_view(), name='oembed'),

]