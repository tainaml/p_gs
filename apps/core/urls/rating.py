from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from apps.core.views.rating import CourseRating

urlpatterns = [

    url(_(r'^rate/$'), CourseRating.as_view(), name='rate'),
]