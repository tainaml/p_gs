from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from apps.core.views import company


urlpatterns = [
    url(_(r'^create$'), company.CompanyEditView.as_view(), name='create'),
]
