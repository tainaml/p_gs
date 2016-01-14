from django.conf.urls import url

from apps.core.views import search as CoreSearch

urlpatterns = [

    url(r'^search$', CoreSearch.Search.as_view(), name='search'),
    url(r'^search/autocomplete$', CoreSearch.SearchAutocomplete.as_view(), name='autocomplete'),
    url(r'^search/list/(?P<content_type>[a-z]+)$', CoreSearch.SearchList.as_view(), name='list'),
    url(r'^search/(?P<content_type>[a-z]+)$', CoreSearch.SearchContent.as_view(), name='search-content'),
]