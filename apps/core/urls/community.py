from django.conf.urls import url
from ..views.community import views, CoreArticleView

view_community_show = CoreArticleView.as_view()

urlpatterns = [
    url(r'^(?P<community_slug>[a-z0-9]+(?:(-|_)[a-z0-9]+)*)$', view_community_show, name='show'),
    ]