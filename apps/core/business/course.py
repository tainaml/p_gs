import copy
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from apps.core.models.course import Course

def get_paginate_list(list=None, items_per_page=None, page=None):
    paginated_items = Paginator(list, items_per_page)

    try:
        paginated_items = paginated_items.page(page)
    except PageNotAnInteger:
        paginated_items = paginated_items.page(1)
    except EmptyPage:
        paginated_items = []

    return paginated_items

def get_courses(itens_per_page=None, **cleaned_data):

    criteria  = copy.copy(cleaned_data)
    del criteria['page']

    return get_items(Course, **criteria)


def get_items(model_class=None, order=None, items_per_page=None, page=None, **criteria):

    items = model_class.objects.filter(**criteria).order_by(order)
    return get_paginate_list(list=items, items_per_page=items_per_page, page=page)



