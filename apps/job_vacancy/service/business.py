from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from ..models import JobVacancy


def get_jobs(keywords=None, locale=None, items_per_page=None, page=None):
    char_to_split = ","
    list_keywords = keywords.split(char_to_split)
    list_locales = locale.split(char_to_split)
    criteria = None
    criteria_location = None

    for keyword in list_keywords:
        if keyword.isnumeric():
            value = float(keyword)
            query_criteria = (
                Q(salary__fixed_value=value) | (
                    Q(salary__range_value_from__lte=value) &
                    Q(salary__range_value_to__gte=value)
                )
            )
        else:
            query_criteria = (
                Q(title__unaccent__icontains=keyword) |
                Q(company__name__unaccent__icontains=keyword) |
                Q(regime__description__unaccent__icontains=keyword) |
                Q(benefits__description__unaccent__icontains=keyword) |
                Q(resposibility__responsibility__name__unaccent__icontains=keyword) |
                Q(resposibility__responsibility_type__description__unaccent__icontains=keyword) |
                Q(requirements__item__description__unaccent__icontains=keyword) |
                Q(requirements__level__description__unaccent__icontains=keyword)
            )
        criteria = query_criteria if not criteria else criteria & query_criteria

    for location in list_locales:
        query_criteria_location = (
            Q(locations__cities__name__unaccent__icontains=location) |
            Q(locations__state__name__unaccent__icontains=location) |
            Q(locations__country__name__unaccent__icontains=location)
        )
        criteria_location = query_criteria_location if not criteria_location \
            else criteria_location | query_criteria_location

    jobs = JobVacancy \
        .objects \
        .filter(criteria & criteria_location) \
        .order_by('-job_vacancy_date') \
        .distinct('id', 'job_vacancy_date')

    if items_per_page and page:
        jobs = Paginator(jobs, items_per_page)

        try:
            jobs = jobs.page(page)
        except PageNotAnInteger:
            jobs = jobs.page(1)
        except EmptyPage:
            jobs = []

    return jobs


def get_job(job_id, slug=None):
    criteria = Q(id=job_id)

    if slug:
        criteria &= Q(slug=slug)

    try:
        job = JobVacancy.objects.get(criteria)
    except JobVacancy.DoesNotExist:
        job = None

    return job
