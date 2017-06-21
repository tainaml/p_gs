from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page
from ..views import community as CoreViews
from ..views import search
urlpatterns = [

    url(r'community/list-all/$', CoreViews.CoreGetCommunities.as_view(), name='list-all'),

    # Translators: URL de pagina de busca da comunidade
    url(_(r'^search/$'), CoreViews.CoreCommunitySearch.as_view(), name='general-search'),

    #Translators: URL de pagina de filtros de comunidades
    url(_(r'^search/community/list/$'), search.SearchCommunitiesList.as_view(), name='search-filter'),

    # Translators: URL de pagina principal de comunidade
    url(_(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)$'), CoreViews.CoreCommunityFeedView.as_view(), name='show-whithout-bar'),

    # Translators: URL de pagina principal de comunidade without bar
    url(_(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/$'), CoreViews.CoreCommunityFeedView.as_view(), name='show'),

    # Translators: URL de pagina principal de comunidade without bar
    url(_(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/cursos/$'), CoreViews.CoreCommunityCourses.as_view(), name='courses'),

    # Translators: URL de sobre da comunidade
    url(_(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/about/$'), CoreViews.CoreCommunityAboutView.as_view(), name='about'),

    # Translators: URL de seguidores da comunidade
    url(_(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/followers/$'), CoreViews.CoreCommunityFollowersView.as_view(), name='followers'),

    # Translators: URL de pagina de busca da comunidade
    url(_(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/search/$'), CoreViews.CoreCommunitySearch.as_view(), name='search'),

    # Translators: URL de listagem da comunidade

    # Translators: URL de perguntas da comunidade
    url(_(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/questions/$'), CoreViews.CoreCommunityQuestionFeedView.as_view(), name='questions'),

    # Translators: URL de pagina de pesquisa de perguntas na comunidade
    url(_(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/questions/search/$'), CoreViews.CoreCommunityQuestionSearch.as_view(), name='questions-search'),

    # Translators: URL de pagina de listagem de perguntas da comunidade
    url(_(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/questions/list/$'), CoreViews.CoreCommunityQuestionList.as_view(), name='questions-list'),

    # Translators: URL de pagina de videos da comunidade
    url(_(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/videos/$'), CoreViews.CoreCommunityVideosView.as_view(), name='videos'),

    # Translators: URL de pagina de procura de videos da comunidade
    url(_(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/videos/search/$'), CoreViews.CoreCommunityVideosSearch.as_view(), name='videos-search'),

    # Translators: URL de pagina de listagem de videos da comunidade
    url(_(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/videos/list/$'), CoreViews.CoreCommunityVideosList.as_view(), name='videos-list'),

    # Translators: URL de pagina de comunidades relacionadas
    url(_(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/related/$'), CoreViews.CommunityRelated.as_view(), name='related'),

    # Translators: URL de pagina checagem de seguidores da comunidade
    url(_(r'^check/user-follows/$'), CoreViews.CommunityCheckUserFollows.as_view(), name='check-user-follows'),

    # Translators: URL de pagina de carregamento assincrono
    url(_(r'^load/async/(?P<object_id>[0-9]+)/(?P<content_type>[a-z]+)/$'), CoreViews.CoreCommunityLoad.as_view(), name='load-communities-async'),

    # Translators: URL de pagina de procura de seguidores da comunidade
    url(_(r'^search/followers$'), CoreViews.CoreCommunityFollowersSearch.as_view(), name='search-followers'),

    # Translators: URL de pagina de listagem de seguidores da comunidade
    url(_(r'^search/followers/list$'), CoreViews.CoreCommunityFollowersSearchList.as_view(), name='search-followers-list'),

    # Translators: URL de pagina de materials da comunidade
    url(_(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/materials/$'), CoreViews.CoreCommunityMaterialsView.as_view(), name='materials'),

    # Translators: URL de pagina de procura de videos da comunidade
    url(_(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/materials/search/$'), CoreViews.CoreCommunityMaterialsSearch.as_view(), name='materials-search'),

    # Translators: URL de pagina de listagem de videos da comunidade
    url(_(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/materials/list/$'), CoreViews.CoreCommunityMaterialsList.as_view(), name='materials-list'),



]