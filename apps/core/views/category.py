from apps.article.models import Article
from apps.core.business.content_types import ContentTypeCached
from django.core.cache import cache
from django.db.models import Q, Prefetch
from django.http import Http404
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import View
from django.utils.translation import gettext
from apps.community.models import Community
from apps.core.forms.category import ListArticleCommunityForm
from apps.custom_base.views import FormBaseListView

from apps.taxonomy.models import Taxonomy


class CoreCategoryPageView(View):

    LIMIT_ITEMS = 11

    base_template = 'home/categorias/%s.html'
    default_template = 'default'
    category = None
    context = {}

    def __init__(self, **kwargs):
        super(CoreCategoryPageView, self).__init__(**kwargs)

    def get_template(self):
        templates = []

        if self.category:
            templates.append(self.base_template % str(self.category.slug))
            pass

        templates.append(self.base_template % self.default_template)

        return templates

    def get_context(self, context=None):
        if context and isinstance(context, list):
            self.context.update(context)

        return self.context

    def get_communities(self):
        communities_filters = Q(taxonomy__parent=self.category) | Q(taxonomy=self.category)
        communities = Community.objects.filter(communities_filters)
        return communities

    def get_feed(self):

        cache_key = 'gsti|excludes|{}'.format(self.category.slug)
        cached_feed = cache.get(cache_key)
        if cached_feed:
            return cached_feed

        communities = self.get_communities()
        article_type = ContentTypeCached.objects.get(model="article")

        articles = Article.objects.filter(
            Q(
                feed__official=True,
                feed__communities__in=communities,
                status__in=[Article.STATUS_PUBLISH],
                feed__content_type=article_type,
                publishin__lte=timezone.now(),
            )
        ).order_by(
            '-publishin'
        ).prefetch_related(
            Prefetch('feed__communities', queryset=communities),
        ).distinct()[0:self.LIMIT_ITEMS]

        cache.set(cache_key, articles, 500)

        return articles


    def get(self, request, category_slug):

        try:

            self.category = Taxonomy.objects.prefetch_related(
                'community_related'
            ).select_related(
                'community_related'
            ).get(
                slug=category_slug,
                term__slug='categoria'
            )

            # self.category.community_related = Community.objects.get(slug=category_slug, taxonomy__term__slug='categoria')
        except Taxonomy.DoesNotExist:
            raise Http404(gettext('Category not found or not root category.'))

        self.get_context().update({
            'category': self.category,
            'category_slug': category_slug,
            'articles': self.get_feed()
        })

        return render(request, self.get_template(), self.get_context())


class ArticleCommunityList(FormBaseListView):
    success_template_path = 'home/categorias/community-list.html'
    form = ListArticleCommunityForm
    itens_per_page = 10
    category = None

    # @Override
    def after_process(self, request=None, *args, **kwargs):
        # print request
        super(ArticleCommunityList, self).after_process(request, *args, **kwargs)
        self.context.update({'communities': self.process_return, 'category_id': request.GET['category_id']})






