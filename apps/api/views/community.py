from apps.api.serializers.community import CommunitySerializer
from apps.community.models import Community
from ..pagination import CommunityResultsSetPagination
from rest_framework import viewsets

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class CommunityViewset(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    pagination_class = CommunityResultsSetPagination

    _30_MINUTUES = 60 * 60 * 30

    @method_decorator(cache_page(_30_MINUTUES))
    def dispatch(self, request, *args, **kwargs):
        return super(CommunityViewset, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = CommunityViewset.queryset

        term = self.request.query_params.get('term', None)

        if term not in [None, ""]:
            queryset = queryset.filter(taxonomy__term__slug=term)



        return queryset.order_by('-id')
