from django.conf import settings
from django.core import urlresolvers
from django.template.defaultfilters import slugify


def generate_home_cache_key(request):

    if request.path == u'/':
        cache_home_page = 'home'
    else:
        _slug_path = slugify(request.path)
        cache_home_page = _slug_path if len(_slug_path) > 0 else 'home'

    return cache_home_page


def build_absolute_uri(path):

    site_url = getattr(settings, 'SITE_URL', False)

    if site_url:
        return '{site}{path}'.format(
            site=site_url,
            path=path
        )
    else:
        from django.contrib.sites.models import Site
        site = Site.objects.get_current()

        return '{protocol}://{domain}{path}'.format(
            protocol=getattr(settings, 'SITE_PROTOCOL', 'http'),
            domain=site.domain,
            path=path
        )

def reverse_absolute(request, path):
    return build_absolute_uri(path)