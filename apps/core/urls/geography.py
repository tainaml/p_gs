from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from apps.core.views.geography import Search


urlpatterns = [
    url(_(r'^(?P<model>\w+)$'), Search.as_view(), name='search')
]