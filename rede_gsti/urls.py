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
from django.views.decorators.cache import cache_page
from apps.core.views.core import Home
from apps.core.views import search as CoreSearch
from apps.core.views.frontend import FrontEndBase
from django.contrib.sitemaps import views as sitemap_views
from apps.core.sitemap import sitemaps
from rede_gsti.urls_old import urls_old
from django.views.generic import RedirectView

handler400 = "apps.core.views.errors.handler400"
handler403 = "apps.core.views.errors.handler403"
handler404 = "apps.core.views.errors.handler404"
handler500 = "apps.core.views.errors.handler500"

url_statics = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
url_media = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
url_search_all = [url(r'(?P<params>.*)$', CoreSearch.SearchAll.as_view(), name='search_all')]
url_job_vacancy = url(_(r'^jobs/'), include('apps.core.urls.jobs_temporary', namespace='jobs'))\
                   if settings.ENVIRONMENT == 'production' else url(_(r'^jobs/'), include('apps.job_vacancy.urls', namespace='jobs'))

urlpatterns = [

    url(r'^$', Home.as_view(), name='index'),
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(_(r'^admin/'), include(admin.site.urls)),

    # Job vacancy
    url_job_vacancy,

    # Translators: URL root de conta
    url(_(r'^account/'), include('apps.core.urls.account', namespace='account')),

    # Translators: URL root de comentario
    url(_(r'^comment/'), include('apps.comment.urls', namespace='comment')),

    # Translators: URL root de perfil de usuario
    url(_(r'^profile/'), include('apps.core.urls.user', namespace='profile')),

    # Translators: URL root de company-organization
    url(_(r'^organization/'), include('apps.core.urls.company', namespace='organization')),

    # Translators: URL de conta social
    url(_(r'^socialaccount/'), include('apps.socialaccount.urls', namespace='socialaccount')),

    # Translators: URL de acoes sociais
    url(_(r'^socialactions/'), include('apps.socialactions.urls', namespace='socialactions')),

    # Translators: URL root de redes sociais
    url('', include('social.apps.django_app.urls', namespace='social')),

    # Translators: URL root de notificacoes
    url(_(r'^notifications/'), include('apps.core.urls.notifications', namespace='notifications')),

    # Translators: URL root de notificacoes
    url(_(r'^hint/'), include('apps.core.urls.hint', namespace='hint')),

    #FIXED ARTICLES REDIRECTS
    url('2011/02/importancia-das-certificacoes.html', RedirectView.as_view(url="/2011/06/importancia-da-certificacao-em-ti-iso.html", permanent=True)),
    url('2012/10/gerenciamento-de-problemas-em-pequenas.html', RedirectView.as_view(url="/2015/11/gerenciamento-de-problemas-em-pequenas-organizacoes.html", permanent=True)),
    url('2013/09/simulado-cobit5.html', RedirectView.as_view(url="/2009/10/simulado-cobit-foundation-5.html", permanent=True)),
    url('2013/02/itil-computacao-em-nuvem.html', RedirectView.as_view(url="/2011/06/computacao-em-nuvem-e-itil-cloud.html", permanent=True)),
    url('2013/02/cloud-computing-foundation.html', RedirectView.as_view(url="/2014/11/itil-e-cloud-computing-video-1724.html", permanent=True)),
    url(r'2012/09/itil-v3-2011.html', RedirectView.as_view(pattern_name='article:view', permanent=True), {'slug': "itil-v3-2011", 'year': "2012", 'month': '04'}),
    url(r'2011/07/tcc-monografia-em-itil-2.html', RedirectView.as_view(pattern_name='article:view', permanent=True), {'slug': "tcc-monografia-em-itil-2", 'year': "2012", 'month': '09'}),
    url(r'2009/09/principais-desafios-da-ti-iii.html', RedirectView.as_view(pattern_name='article:view', permanent=True), {'slug': "principais-desafios-da-ti-ii", 'year': "2009", 'month': '09'}),
    url(r'2016/10/10-passos-para-elaborar-um-plano-da-capacidade-de-ti.html', RedirectView.as_view(pattern_name='article:view', permanent=True), {'slug': "10-passos-para-elaborar-um-plano-da-capacidade-de-ti", 'year': "2012", 'month': '08'}),
    url(r'2011/07/simulado-iso-27002-foundation-2.html', RedirectView.as_view(pattern_name='article:view', permanent=True), {'slug': "simulado-iso-27002", 'year': "2011", 'month': '04'}),

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

    # Translators: URL root de amp
    url(_(r'^'), include('apps.core.urls.amp', namespace='amp')),

    # Translators: URL root of user alerts
    url(_(r'^useralerts/'), include('apps.useralerts.urls', namespace='useralerts')),

    # Translators: URL de curso
    url(_(r'^courses/'), include('apps.core.urls.course', namespace='course')),

    # Translators: URL de curso
    url(_(r'^rating/'), include('apps.core.urls.rating', namespace='rating')),

    # Translators: URL core adicionais
    url(_(r'^'), include('apps.core.urls.core', namespace='core')),

    url(r'^chaining/', include('smart_selects.urls')),

    # Translators: URL de buscai
    url(_(r'^'), include('apps.core.urls.search', namespace='search')),

    # Translators: URL core adicionais
    url(_(r'^'), include('apps.core.urls.core', namespace='core')),

    # Translators: URL root de comunidade
    url(_(r'^'), include('apps.core.urls.community', namespace='community')),

    url(r'^ideia-summernote/', include('apps.core.urls.summernote', namespace='ideia-summernote')),

    url(r'^sitemap\.xml$', sitemap_views.index, {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', cache_page(settings.TIME_TO_REFRESH_SITEMAP)(sitemap_views.sitemap), {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    url(r'^', include('apps.core.urls.blogspot', namespace='blogspot')),

] + url_statics + url_media + urls_old
urls_front_end = [
    url(_(r'^front-end/(?P<template>[a-z0-9./]+(?:(-|_)[a-z0-9.]+)*)'), FrontEndBase.as_view())
]

if not (settings.ENVIRONMENT=='production'):
    urlpatterns += urls_front_end

if hasattr(settings, 'PROFILER_APP') and getattr(settings, 'PROFILER_APP') == 'silk' and getattr(settings, 'ENVIRONMENT') == 'develop':
    urlpatterns += [
        url(r'^admin/silk/', include('silk.urls', namespace='silk'))
    ]
urlpatterns += url_search_all
