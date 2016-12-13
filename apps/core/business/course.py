from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from apps.core.models.course import Course
from apps.taxonomy.models import Taxonomy



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

    filters = {}
    criteria = Q(active=True)
    if cleaned_data.get('title'):
        criteria = criteria & Q(title__icontains=cleaned_data.get('title'))

    if cleaned_data.get('category'):
        criteria = criteria & (Q(taxonomies__parent=Taxonomy.objects.filter(slug=cleaned_data['category']))
                               | Q(taxonomies=Taxonomy.objects.filter(slug=cleaned_data['category'])))

    if cleaned_data.get('community'):
        criteria = criteria & Q(taxonomies=Taxonomy.objects.filter(slug=cleaned_data['community']))

    order = cleaned_data.get('order') or "-rating"

    #TODO verify why is repeating rows
    items = Course.objects.filter(criteria).prefetch_related("taxonomies", "languages", "internal_author__profile").distinct("id", order.replace("-", "")).order_by(order)

    return get_paginate_list(list=items, items_per_page=itens_per_page, page=cleaned_data['page'])


def get_items(model_class=None, order=None, items_per_page=None, page=None, **criteria):


    items = model_class.objects.all()
    if criteria:
        items.filter(**criteria)


    return get_paginate_list(list=items, items_per_page=items_per_page, page=page)



