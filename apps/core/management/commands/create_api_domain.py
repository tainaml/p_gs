from django.core.management import BaseCommand
from django.conf import settings
import os

API_PATH = os.path.join(settings.BASE_DIR, "apps", "api")

URLS_INIT = os.path.join(API_PATH, "urls", "__init__.py")
URL_APPEND_STRING = "\n[urlpatterns += [url(r'^{0}/', include('apps.api.urls.{1}', namespace='{1}'))]"

VIEW_PATH = os.path.join(API_PATH, "views", "{0}.py")
URL_PATH = os.path.join(API_PATH, "urls", "{0}.py")
SERIALIZER_PATH = os.path.join(API_PATH, "serializers", "{0}.py")

PAGINATION = os.path.join(API_PATH, "pagination.py")

PAGINATION_CODE = """\n\n
class {0}ResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

"""

SERIALIZER_CODE = """

from rest_framework import serializers


class {0}Serializer(serializers.ModelSerializer):


    class Meta:
        model = {0}
        fields = (
            'field',

        )
        read_only_fields = None
"""

URL_CODE = """

from django.conf.urls import url
from ..views import {0}

urlpatterns = [
    url(r"^$", {0}.{1}Viewset.as_view({{
        "get": "list"
    }}), name='list'),
    url(r"^(?P<pk>\d+)/$", {0}.{1}Viewset.as_view(
        {{
            "get":  "retrieve"
        }}
    ), name="retrieve"),


]

"""

VIEW_CODE = """
from django.http.response import Http404
from ..pagination import StandardResultsSetPagination, FeedResultsSetPagination
from rest_framework import viewsets
from django.contrib.admin.models import ContentType
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class {0}Viewset(viewsets.ModelViewSet):
    queryset = {0}.objects.all()
    serializer_class = {0}Serializer
    pagination_class = {0}ResultsSetPagination


    @method_decorator(cache_page(10))
    def dispatch(self, request, *args, **kwargs):
        return super({0}Viewset, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = {0}Viewset.queryset


        param = self.request.query_params.get('param', None)

        if param is not None:
            queryset = queryset.filter(param=param)



        return queryset.order_by('-id')
"""

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('domain', nargs='+', type=str)


    def handle(self, *args, **options):
        domain =  options['domain'][0]

        domain_class = domain
        domain_lower = domain.lower()
        domain_plural = domain.lower() + "s"

        # URLS INIT
        with open(URLS_INIT,'a') as f:
            f.write(URL_APPEND_STRING.format(domain_plural, domain_lower))
            f.close()

        # View
        with open(VIEW_PATH.format(domain_lower),'wb') as f:
            f.write(VIEW_CODE.format(domain_class))
            f.close()

        # URL
        with open(URL_PATH.format(domain_lower),'wb') as f:
            f.write(URL_CODE.format(domain_lower, domain_class))
            f.close()

        # Serializer
        with open(SERIALIZER_PATH.format(domain_lower),'wb') as f:
            f.write(SERIALIZER_CODE.format(domain_class))
            f.close()

        # PAGINATION
        with open(PAGINATION,'a') as f:
            f.write(PAGINATION_CODE.format(domain_class))
            f.close()

