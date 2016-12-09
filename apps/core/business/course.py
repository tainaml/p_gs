from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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
    if cleaned_data.get('title'):
        filters['title__contains']= cleaned_data.get('title')

    if cleaned_data.get('category'):
        filters['taxonomies__parent']= Taxonomy.objects.filter(slug=cleaned_data['category'])

    if cleaned_data.get('community'):
        filters['taxonomies']= Taxonomy.objects.filter(slug=cleaned_data['community'])

    order = cleaned_data.get('order') or "-updatein"


    items = Course.objects.filter(**filters).prefetch_related("taxonomies", "languages", "internal_author__profile").order_by(order)

    return get_paginate_list(list=items, items_per_page=itens_per_page, page=cleaned_data['page'])


def get_items(model_class=None, order=None, items_per_page=None, page=None, **criteria):


    items = model_class.objects.all()
    if criteria:
        items.filter(**criteria)


    return get_paginate_list(list=items, items_per_page=items_per_page, page=page)



