from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from apps.core.models.course import Course

__author__ = 'phillip'

def paginate_list(list=None, itens_per_page=None):
    paginated_items = Paginator(list, itens_per_page)

    try:
        paginated_items = paginated_items.page(page)
    except PageNotAnInteger:
        paginated_items = paginated_items.page(1)
    except EmptyPage:
        paginated_items = []

    return paginated_items

def get_courses(itens_per_page=None, **cleaned_data):
    course_filter = Q()
    course_order = ("")
    courses = Course.objects.filter(course_filter).order_by(course_order)



