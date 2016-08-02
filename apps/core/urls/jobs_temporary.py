#'jobs:index'
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.shortcuts import redirect


def __redirect_jobs_index(response):
    return redirect(reverse('community:show', args=['vagas-de-trabalho']))


urlpatterns = [
    url(r'^$', __redirect_jobs_index, name='index'),
]