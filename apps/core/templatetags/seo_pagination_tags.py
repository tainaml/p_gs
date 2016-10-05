from django import template

register = template.Library()
PAGE_INCREMENT = 1

@register.inclusion_tag('core/templatetags/seo-links.html', takes_context=True)
def pagination_links(context, items):

    request = context['request']

    next_page_params = request.GET.copy()
    previous_page_params = request.GET.copy()

    page = request.GET.get("page")

    try:
        page = int(page)
    except TypeError:
        page = None
    except ValueError:
        page = None

    if items and items.has_next():
        page  = page if page else 1
        next_page_params['page']= page + PAGE_INCREMENT

        next_page_params = next_page_params.urlencode()

    else:
        next_page_params = None

    if items and items.has_previous() and page:
        previous_page_params['page']= page - PAGE_INCREMENT
        previous_page_params = previous_page_params.urlencode()

    else:
        previous_page_params = None


    return {
        "request": request,
        "next_page_params": next_page_params,
        "previous_page_params": previous_page_params

    }