from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from apps.core.views import superuser as SU

urlpatterns = [

    # Translators: Url de push
    url(_(r'^push$'), SU.AdminPush.as_view(), name='push'),

]