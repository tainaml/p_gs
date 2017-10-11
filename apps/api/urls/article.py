

from django.conf.urls import url
from ..views import article

urlpatterns = [
    url(r"^$", article.ArticleViewset.as_view({
        "get": "list"
    }), name='list'),
    url(r"^(?P<pk>\d+)/$", article.ArticleViewset.as_view(
        {
            "get":  "retrieve"
        }
    ), name="retrieve"),


]

