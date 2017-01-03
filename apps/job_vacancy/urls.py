from django.conf.urls import url

from . import views
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^(?P<job_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/(?P<job_id>[0-9]+)$', views.JobDetailView.as_view(), name='detail'),
    url(r'^search$', views.JobView.as_view(), name='search'),
    url(r'^list$', views.JobListView.as_view(), name='list'),
    # url(r'^$', views.JobView.as_view(), name='index'),
    url(r'^$', RedirectView.as_view(pattern_name='community:show'), {'community_slug': "vagas-de-trabalho"}, name='index')
]
