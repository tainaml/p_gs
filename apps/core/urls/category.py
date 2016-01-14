from django.conf.urls import url

from ..views import category as CategoryView

urlpatterns = [
    url(r'^(?P<category_slug>[a-z0-9]+(?:-[a-z0-9]+)*)/$', CategoryView.CoreCategoryPageView.as_view(), name='show'),
]