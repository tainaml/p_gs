"""rede_gsti URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from apps.ninico.views import index as PROJECT_ROOT
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache

handler400 = "apps.core.views.errors.handler400"
handler403 = "apps.core.views.errors.handler403"
handler404 = "apps.core.views.errors.handler404"
handler500 = "apps.core.views.errors.handler500"

url_statics = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
url_media = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from apps.core.views import editor as EDITOR_VIEW
from apps.core.views import search as CoreSearch

urlpatterns = [



    url(r'^$', PROJECT_ROOT, name='index'),
    url(_(r'^admin/'), include(admin.site.urls)),

    # Job vacancy
    url(_(r'^jobs/'), include('apps.core.urls.jobs_temporary', namespace='jobs')),

    # Translators: URL root de conta
    url(_(r'^account/'), include('apps.core.urls.account', namespace='account')),

    # Translators: URL root de comentario
    url(_(r'^comment/'), include('apps.comment.urls', namespace='comment')),

    # Translators: URL root de perfil de usuario
    url(_(r'^profile/'), include('apps.core.urls.user', namespace='profile')),

    # Translators: URL de conta social
    url(_(r'^socialaccount/'), include('apps.socialaccount.urls', namespace='socialaccount')),

    # Translators: URL de acoes sociais
    url(_(r'^socialactions/'), include('apps.socialactions.urls', namespace='socialactions')),

    # Translators: URL root de redes sociais
    url('', include('social.apps.django_app.urls', namespace='social')),



    # Translators: URL root de notificacoes
    url(_(r'^notifications/'), include('apps.core.urls.notifications', namespace='notifications')),

    # Translators: URL root de publicacao
    url(_(r'^'), include('apps.core.urls.article', namespace='article')),

    # Translators: URL root CORE de acoes sociais
    url(_(r'^'), include('apps.core.urls.socialactions', namespace='core_socialactions')),

    # Translators: URL root de categoria
    url(_(r'^category-feed/'), include('apps.core.urls.category', namespace='category')),

    # Translators: URL root de pergunta
    url(_(r'^question/'), include('apps.core.urls.question', namespace='question')),

    # Translators: URL root de contato
    url(_(r'^contact/'), include('apps.core.urls.contact', namespace='contact')),

    # Translators: URL root de contato
    url(_(r'^mailmanager/'), include('apps.mailmanager.urls', namespace='mailmanager')),

    # Translators: URL root de denuncia
    url(_(r'^complaint/'), include('apps.complaint.urls', namespace='complaint')),

    # Translators: URL root de configuracao
    url(_(r'^settings/'), include('apps.core.urls.configuration', namespace='configuration')),


    # Translators: URL root de feed
    url(_(r'^feed/'), include('apps.core.urls.feed', namespace='feed')),

    # Translators: URL de buscai
    url(_(r'^'), include('apps.core.urls.search', namespace='search')),

    # Translators: URL core adicionais
    url(_(r'^'), include('apps.core.urls.core', namespace='core')),

    # Translators: URL do ckeditor
    url(r'^/editor/upload/', staff_member_required(EDITOR_VIEW.upload), name='ckeditor_upload'),
    # url(r'^/editor/browse/', never_cache(staff_member_required(views.browse)), name='ckeditor_browse'),

     url(r'^chaining/', include('smart_selects.urls')),

    # Translators: URL root de comunidade
    url(_(r'^'), include('apps.core.urls.community', namespace='community')),

    url(r'(?P<params>.*)$', CoreSearch.SearchAll.as_view(), name='search_all'),

] + url_statics + url_media
