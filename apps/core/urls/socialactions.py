from django.conf.urls import url
from apps.core.views import socialactions

urlpatterns = [

    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/perfil/ver-depois/$', socialactions.SocialActionSeeLater.as_view(), name='see_later'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/perfil/remover-ver-depois/$', socialactions.SocialActionRemoveSeeLater.as_view(), name='remove_see_later'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/perfil/favoritos/$', socialactions.SocialActionFavourite.as_view(), name='favourite'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/perfil/desfavoritar/$', socialactions.SocialActionRemoveFavourite.as_view(), name='unfavourite'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/perfil/sugestoes/$', socialactions.SocialActionSuggest.as_view(), name='suggest'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/perfil/remover-sugestao/$', socialactions.SocialActionRemoveSuggest.as_view(), name='unsuggest'),

    url(r'^filter/followings/$', socialactions.SocialActionFilterFollowings.as_view(), name='filter_followings'),

]

