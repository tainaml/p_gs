from django.conf.urls import url

from views import Show

urlpatterns = [
    url(r'^show/(?P<alert_id>\d+)$', Show.as_view(), name='show'),
]