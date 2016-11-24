__author__ = 'phillip'

from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from apps.core.views.course import CourseListView,CourseShowView

urlpatterns = [
         url(_(r'^(?P<course_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)/$'), CourseShowView.as_view(), name='show'),
         url(_(r'^'), CourseListView.as_view(), name='list'),

]