from django.template.defaultfilters import slugify


def generate_home_cache_key(request):

    if request.path == u'/':
        cache_home_page = 'home'
    else:
        _slug_path = slugify(request.path)
        cache_home_page = _slug_path if len(_slug_path) > 0 else 'home'

    return cache_home_page