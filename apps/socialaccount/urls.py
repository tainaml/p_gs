from django.conf.urls import url, include

urlpatterns = [

    url(r'^$', 'apps.socialaccount.views.home', name='index'),
    url(r'^home/', 'apps.socialaccount.views.home', name="home"),
    url(r'^email-sent/', 'apps.socialaccount.views.validation_sent'),
    url(r'^login/$', 'apps.socialaccount.views.home'),
    url(r'^logout/$', 'apps.socialaccount.views.logout'),
    url(r'^done/$', 'apps.socialaccount.views.done', name='done'),
    url(r'^ajax-auth/(?P<backend>[^/]+)/$', 'apps.socialaccount.views.ajax_auth', name='ajax-auth'),
    url(r'^email/$', 'apps.socialaccount.views.require_email', name='require_email'),

]