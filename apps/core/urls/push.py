from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from ..views import push

urlpatterns = [

    url(_(r'^subscribe/$'), push.ReceiveSubscribe.as_view(), name='subscribe'),


]
