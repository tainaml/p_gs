__author__ = 'phillip'

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from . import views

urlpatterns = [

    # Translators: URL de acao social
    url(_(r'^act/(?P<object_to_link>[0-9]+)/(?P<content>[a-zA-Z]+)/(?P<action>[a-z0-9]+(?:-[a-z0-9]+)*)'), views.SocialActionView.as_view(), name='act'),

    # Translators: URL de acao social ajax
    url(_(r'^act/xhr/(?P<object_to_link>[0-9]+)/(?P<content>[a-zA-Z]+)/(?P<action>[a-z0-9]+(?:-[a-z0-9]+)*)'), views.SocialActXHR.as_view(), name='act-xhr'),

    # Translators: URL para saber se o usuario agiu sobre um determinado item
    url(_(r'^acted/(?P<object_to_link>[0-9]+)/(?P<content>[a-zA-Z]+)/(?P<action>[a-z0-9]+(?:-[a-z0-9]+)*)'), views.SocialUserActed.as_view(), name='acted'),

    # Translators: URL de acao social ajax
    url(_(r'^act/ajax/(?P<object_to_link>[0-9]+)/(?P<content>[a-zA-Z]+)/(?P<action>[a-zA-Z]+)'), views.SocialActionAjax.as_view(), name='act-ajax'),

    # Translators: URL de sugerir
    url(_(r'^act/suggest/(?P<object_to_link>[0-9]+)/(?P<content>[a-z]+)/$'), views.SocialActionSuggestArticleToUser.as_view(), name='act-suggest'),

    # Translators: URL de seguidores
    url(_(r'^followers/(?P<content_type_id>[0-9]+)/(?P<object_filter_id>[0-9]+)/$'), views.SocialActionFollowersViews.as_view(), name='get_followers'),

    # Translators: URL de seguindo
    url(_(r'^followings/(?P<content_type_id>[0-9]+)/(?P<object_filter_id>[0-9]+)/$'), views.SocialActionFollowingsViews.as_view(), name='get_followings'),

]