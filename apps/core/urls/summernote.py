from django.conf.urls import url
from ..views.summernote import CoreUpload
urlpatterns = [
    url(r'^upload', CoreUpload.as_view(), name='upload'),

]