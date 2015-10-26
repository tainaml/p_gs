from django.conf.urls import url
from apps.core.views import socialactions

urlpatterns = [

    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/perfil/ver-depois/$', socialactions.SocialActionSeeLater.as_view(), name='see_later'),
    url(r'^(?P<username>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/perfil/remover-ver-depois/$', socialactions.SocialActionRemoveSeeLater.as_view(), name='remove_see_later'),
]

