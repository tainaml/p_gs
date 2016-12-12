from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from apps.core.views import course as courseViews
from apps.core.views.course import CourseRate

urlpatterns = [

    url(_(r'^course/rate/$'), CourseRate.as_view(), name='course'),
    url(_(r'^course/rate/(?P<rate_id>\d+)/delete$'), courseViews.CourseRateDelete.as_view(), name='course-delete'),
]