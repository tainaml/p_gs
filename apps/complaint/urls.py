from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from . import views

urlpatterns = [

    # url(r'^(?P<complaint>\w{0,50})/$', views.ComplaintView.as_view(), name='report')
    # Translators: URL de denunciar objeto
    url(_(r'^(?P<object_type>[a-z]+)/(?P<object_id>[0-9]+)$'), views.ComplaintView.as_view(), name='report')

]