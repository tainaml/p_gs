from apps.api.serializers.article import ArticleSerializer
from apps.article.models import Article
from django.db.models import Q
from ..pagination import ArticleResultsSetPagination
from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class ArticleViewset(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = ArticleResultsSetPagination


    @method_decorator(cache_page(10))
    def dispatch(self, request, *args, **kwargs):
        return super(ArticleViewset, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):


        queryset = ArticleViewset.queryset.prefetch_related("author", "author__profile")

        queryset = queryset.filter(
            Q(status=Article.STATUS_PUBLISH)
        )

        q = self.request.query_params.get('Q', None)

        if q is not None:

            queryset = queryset.filter(title__icontains=q)



        return queryset.order_by('-id')
