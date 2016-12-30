#'jobs:index'
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from apps.job_vacancy.views import JobDetailView


def __redirect_jobs_index(response):
    return redirect(reverse('community:show', args=['vagas-de-trabalho']))


urlpatterns = [
    url(r'^$', __redirect_jobs_index, name='index'),
    url(r'^/(?P<slug>[a-z0-9./]+(?:(-|_)[a-z0-9.]+)*)/d+$', JobDetailView.as_view(), name='detail'),
]