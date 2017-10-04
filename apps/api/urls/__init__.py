from django.conf.urls import url, include

urlpatterns = [

    url(r'^users/', include('apps.api.urls.user', namespace='user')),
    url(r'^feeds/', include('apps.api.urls.feed', namespace='feed'))
    # url(r'^auth/', include('apps.api.urls.auth', namespace='auth')),


]


urlpatterns += [url(r'^communities/', include('apps.api.urls.community', namespace='community'))]