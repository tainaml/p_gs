from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

urlpatterns = [

    # Translators: URL index de conta social
    url(_(r'^$'), 'apps.socialaccount.views.home', name='index'),

    # Translators: URL de home de conta social
    url(_(r'^home/'), 'apps.socialaccount.views.home', name="home"),

    # Translators: URL de email enviado de conta social
    url(_(r'^email-sent/'), 'apps.socialaccount.views.validation_sent'),

    # Translators: URL de login de conta social
    url(_(r'^login/$'), 'apps.socialaccount.views.home'),

    # Translators: URL de logout de conta social
    url(_(r'^logout/$'), 'apps.socialaccount.views.logout'),

    # Translators: URL de termino de processo de conta social
    url(_(r'^done/$'), 'apps.socialaccount.views.done', name='done'),

    # Translators: URL de autenticacao social ajax
    url(_(r'^ajax-auth/(?P<backend>[^/]+)/$'), 'apps.socialaccount.views.ajax_auth', name='ajax-auth'),

    # Translators: URL de requisicao de email social
    url(_(r'^email/$'), 'apps.socialaccount.views.require_email', name='require_email'),

]