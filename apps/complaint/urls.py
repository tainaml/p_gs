from django.conf.urls import url
from . import views
from . import views

urlpatterns = [
    url(r'', views.ComplaintView.as_view(), name='report'),
]