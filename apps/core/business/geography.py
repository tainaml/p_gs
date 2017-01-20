from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from apps.core.exceptions.geography import NotSearchableModelException
from apps.geography.models import City, Country, State
MODELS_TO_SEARCH = {'country': Country, 'state': State, 'city': City}



def get_geography(model=None, text='', items_per_page=None, page=None):

    if model not in MODELS_TO_SEARCH:
        raise NotSearchableModelException()

    LocaleModel = MODELS_TO_SEARCH[model]
    print LocaleModel
    locales = LocaleModel.objects.filter(name__icontains=text)
    print locales
    items_per_page = items_per_page if items_per_page else 10

    locales = Paginator(locales, items_per_page)

    try:
        paginated = locales.page(page)
    except PageNotAnInteger:
        paginated = locales.page(1)
    except EmptyPage:
        paginated = []

    return paginated