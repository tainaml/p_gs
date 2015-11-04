from django.conf.urls import url
from apps.core.views import search as CoreSearch

urlpatterns = [

    url(r'^search$', CoreSearch.Search.as_view(), name='search'),
    url(r'^search/autocomplete$', CoreSearch.SearchAutocomplete.as_view(), name='autocomplete'),

]

