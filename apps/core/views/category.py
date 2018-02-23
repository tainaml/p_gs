from apps.article.models import Article
from apps.core.business.content_types import ContentTypeCached
from apps.core.templatetags.article_blocks import get_article_community_by_category
from apps.feed.models import FeedObject
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


CACHE_TIME = 60 * 10
CACHE_KEY_TAXONOMY = u'all_categories'

class CoreCategoryPageView(View):

    LIMIT_ITEMS = 11

    base_template = 'home/categorias/%s.html'
    default_template = 'default'
    category = None
    context = {}
    form = ListArticleCommunityForm
    itens_per_page = 5

    def __init__(self, **kwargs):
        super(CoreCategoryPageView, self).__init__(**kwargs)

    def get_template(self):
        templates = []

        if self.category:
            templates.append(self.base_template % str(self.category.slug))

        templates.append(self.base_template % self.default_template)

        return templates

    def get_context(self, context=None):

        QUANTITY = 27

        CACHE_KEY = "home_{0}".format(self.category.slug)
        feed_articles_list = cache.get(CACHE_KEY)



        if not feed_articles_list:

            taxonomy = self.category

            feed_articles = FeedObject.objects.\
            prefetch_related("content_object", "content_type","content_object__author", "content_object__author__profile", "communities", "communities__taxonomy").filter(
            Q(article__status=Article.STATUS_PUBLISH)
            & Q(object_id__isnull=False)
            & Q(official=True)
            & Q(taxonomies=taxonomy)
            ).order_by("-date")[:QUANTITY]
            feed_articles_list = {}

            items = list(reversed(list(feed_articles)))

            feed_articles_list[taxonomy.slug] = {"items": items, "community": taxonomy.community_related}

            cache.set(CACHE_KEY, feed_articles_list, CACHE_TIME)
        self.context.update({"feed_articles_list": feed_articles_list})


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

        for article in articles:

            if not bool(article.image):
                _community = get_article_community_by_category(article, self.category)
                article.image = _community.image if _community and bool(_community.image) else None

        cache.set(cache_key, articles, 0)

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

        page = request.GET.get("page")


        form = self.form(self.itens_per_page, {'category_id': self.category.id,
                                                       'page' : page})
        feed_objects = form.process()

        self.get_context().update({
            'category': self.category,
            'category_slug': category_slug,
            'articles': self.get_feed(),
            'feed_objects': feed_objects,
            'page': form.cleaned_data['page'] +1
        })

        return render(request, self.get_template() if  not request.is_ajax() else 'home/categorias/community-list.html', self.get_context())


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






