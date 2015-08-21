__author__ = 'phillip'
from django.conf.urls import url


urlpatterns = [

    url(r'^signup/', 'apps.account.views', name='signup')

]