from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from apps.core.views import search as CoreSearch

urlpatterns = [

    # Translators: URL de busca geral
    url(_(r'^search$'), CoreSearch.Search.as_view(), name='search'),

    # Translators: URL de autocomplete de busca geral
    url(_(r'^search/autocomplete$'), CoreSearch.SearchAutocomplete.as_view(), name='autocomplete'),

    # Translators: URL de listagem de busca geral
    url(_(r'^search/list/(?P<content_type>[a-z]+)$'), CoreSearch.SearchList.as_view(), name='list'),

    # Translators: URL de procurar conteudo
    url(_(r'^search/(?P<content_type>[a-z]+)$'), CoreSearch.SearchContent.as_view(), name='search-content'),
]