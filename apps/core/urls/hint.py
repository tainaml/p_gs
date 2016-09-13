from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from ..views import hint

urlpatterns = [
    url(r'^(?P<instance_type>[a-z]+)/(?P<instance_id>[0-9]+)$', hint.HintAjaxView.as_view(), name='list'),
]