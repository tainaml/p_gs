from django.conf.urls import url

from apps.core.views import contact as CoreContactViews

urlpatterns = [

    url(r'^$', CoreContactViews.CoreContactView.as_view(), name='create'),
    url(r'^save/$', CoreContactViews.CoreContactSaveViews.as_view(), name='save'),

]