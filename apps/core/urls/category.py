from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from ..views import category as CategoryView

urlpatterns = [

    # Translators: URL de home de categoria
    url(_(r'^(?P<category_slug>[a-z0-9]+(?:-[a-z0-9]+)*)/$'), CategoryView.CoreCategoryPageView.as_view(), name='show'),
    url(_(r'^list-communities-articles$'), CategoryView.ArticleCommunityList.as_view(), name='list-community_articles'),
]