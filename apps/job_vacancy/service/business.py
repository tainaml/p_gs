from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from ..models import JobVacancy


def get_jobs(keyowrs=None, locale=None, items_per_page=None, page=None):

    jobs = JobVacancy.objects.all().order_by('-job_vacancy_date')

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
