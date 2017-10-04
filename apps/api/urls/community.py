

from django.conf.urls import url
from ..views import community

urlpatterns = [
    url(r"^$", community.CommunityViewset.as_view({
        "get": "list"
    }), name='list'),
    url(r"^(?P<pk>\d+)/$", community.CommunityViewset.as_view(
        {
            "get":  "retrieve"
        }
    ), name="retrieve"),


]

