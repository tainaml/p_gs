from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from apps.core.views import socialactions

urlpatterns = [

    # Translators: URL de filtro de seguindo
    url(_(r'^filter/followings/$'), socialactions.SocialActionFilterFollowings.as_view(), name='filter_followings'),

    # Translators: URL de contagem de acoes
    url(_(r'^counter-actions/(?P<username>[a-z0-9_-]+)/(?P<action>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/$'), socialactions.CountActions.as_view(), name='counter-actions'),

]
