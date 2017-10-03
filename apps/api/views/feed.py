from apps.api.serializers.feed import FeedObjectSerializer
from apps.article.models import Article
from apps.feed.models import FeedObject
from django.db.models import Q
from django.http.response import Http404
from ..pagination import StandardResultsSetPagination, FeedResultsSetPagination
from rest_framework import viewsets
from django.contrib.admin.models import ContentType
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class FeedViewset(viewsets.ModelViewSet):
    queryset = FeedObject.objects.all().prefetch_related("content_object", "content_type","content_object__author")
    serializer_class = FeedObjectSerializer
    pagination_class = FeedResultsSetPagination
    ordering_fields = ('date',)


    @method_decorator(cache_page(10))
    def dispatch(self, request, *args, **kwargs):
        return super(FeedViewset, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = FeedViewset.queryset


        queryset = queryset.filter(
            (Q(article__status=Article.STATUS_PUBLISH)
            | Q(question__id__isnull=False)
            | Q(profile_status__status=True))
            & Q(object_id__isnull=False)

        )

        content_type = self.request.query_params.get('content_type', None)
        taxonomies = self.request.query_params.get('taxonomies', None)
        communities = self.request.query_params.get('communities', None)

        official = self.request.query_params.get('official', None)
        object_id = self.request.query_params.get('object_id', None)
        after = self.request.query_params.get('after', None)

        if content_type is not None:
            content_type = content_type.split(":")
            try:
                content_type  = ContentType.objects.get(app_label=content_type[0], model=content_type[1])

                queryset = queryset.filter(content_type=content_type)

            except ContentType.DoesNotExist:

                raise Http404()




        if object_id is not None:
            queryset = queryset.filter(object_id=object_id)

        if taxonomies is not None:
            queryset = queryset.filter(taxonomies__in=taxonomies.split(","))

        if communities is not None:
            queryset = queryset.filter(communities__in=communities.split(","))

        if official is not None:
            queryset = queryset.filter(official=official.lower() == "true")

        if after is not None:
            queryset = queryset.filter(id__gt=after)



        return queryset.order_by('-date')