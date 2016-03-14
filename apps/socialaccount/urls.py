from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from apps.socialaccount import views

urlpatterns = [

    # Translators: URL index de conta social
    url(_(r'^$'), views.home, name='index'),

    # Translators: URL de home de conta social
    url(_(r'^home/'), views.home, name="home"),

    # Translators: URL de email enviado de conta social
    url(_(r'^email-sent/'), views.validation_sent),

    # Translators: URL de login de conta social
    url(_(r'^login/$'), views.home),

    # Translators: URL de logout de conta social
    url(_(r'^logout/$'), views.logout),

    # Translators: URL de termino de processo de conta social
    url(_(r'^done/$'), views.done, name='done'),

    # Translators: URL de autenticacao social ajax
    url(_(r'^ajax-auth/(?P<backend>[^/]+)/$'), views.ajax_auth, name='ajax-auth'),

    # Translators: URL de requisicao de email social
    url(_(r'^email/$'), views.require_email, name='require_email'),

]