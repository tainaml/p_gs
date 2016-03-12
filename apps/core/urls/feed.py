from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from ..views import feed as view

urlpatterns = [
    # Translators: URL de setar conteudo como oficial
    url(_(r'^set-official/(?P<content_type>[a-z]+)/(?P<object_id>[0-9]+)$'), view.FeedContentOfficial.as_view(), name='set-content-official'),

]