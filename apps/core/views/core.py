from apps.article.models import Article
from apps.community.models import Community
from apps.core.business import feed as FeedBusiness
from apps.feed.models import FeedObject
from apps.taxonomy.models import Taxonomy
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.views.generic import View
import micawber
from micawber.providers import Provider
from django.core.cache import cache


class CoreBaseView(View):

    def return_error(self, request, context=None):
        pass


    def return_success(self, request, context=None):
        pass


    def change_template(self, template_path):
        pass


    def get_context(self, request, *args, **kwargs):
        return {}


class CoreRelatedPosts(CoreBaseView):

    template_path = "core/templatetags/related-posts-box.html"

    def return_error(self, request, context=None):
        if not context:
            context = {}

        if request.is_ajax():
            _context = {
                'template': render(request, self.template_path, context).content
            }
            return JsonResponse(_context, status=400)


    def return_success(self, request, context=None):
        if not context:
            context = {}

        if request.is_ajax():
            _context = {
                'template': render(request, self.template_path, context).content
            }
            return JsonResponse(_context, status=200)

    def get(self, request, instance_id, instance_type, post_type=None, count=None):


        count = count if count and count < 10 else 3

        try:

            related_object = FeedBusiness.get_related_posts_from_item(instance_id, instance_type, post_type, count)

        except Exception, e:
            return self.return_error(request, None)

        context = {
            'feed_records': related_object.get('feed_records'),
            'template_path': related_object.get('template_path')
        }

        return self.return_success(request, context)

CACHE_TIME = 60 * 10
CACHE_KEY = u'home_articles'
CACHE_KEY_TAXONOMY = u'all_categories'

class Home(View):

    def get(self, request):
        QUANTITY = 7


        feed_articles_list = cache.get(CACHE_KEY)

        if not feed_articles_list:
            taxonomies = cache.get(CACHE_KEY_TAXONOMY)
            if not taxonomies:
                taxonomies = list(Taxonomy.objects.filter(term__slug="categoria"))
                cache.set(CACHE_KEY_TAXONOMY, taxonomies, CACHE_TIME)
            feed_articles_list = {}
            for taxonomy in taxonomies:
                feed_articles = FeedObject.objects.all().\
                    prefetch_related("content_object", "content_type","content_object__author", "content_object__author__profile", "communities", "communities__taxonomy")
                feed_articles = feed_articles.filter(
                Q(article__status=Article.STATUS_PUBLISH)
                & Q(object_id__isnull=False)
                & Q(official=True)
                & Q(taxonomies=taxonomy)
                )[:QUANTITY]
                feed_articles_list[taxonomy.slug] = {"items": list(feed_articles), "community": Community.objects.filter(taxonomy__slug=taxonomy.slug).prefetch_related("taxonomy").get()}


        return render(request, 'home/index.html', {"feed_articles_list": feed_articles_list})


class About(View):

    def get(self, request):
        return render(request, 'about.html')


class Rules(View):

    def get(self, request):
        return render(request, 'rules.html')

class Privacy(View):

    def get(self, request):
        return render(request, 'privacy.html')


class OEmbed(View):

    def get(self, request):
        url = request.GET.get('url', None)
        if not url:

            return JsonResponse({'success': False, 'message': 'Invalid url.'})

        try:
            providers = micawber.bootstrap_noembed()

            # Custom Providers
            providers.register('http://(\S*.)?youtu(\.be/|be\.com/playlist)\S+', Provider('http://www.youtube.com/oembed'))
            providers.register('https://(\S*.)?youtu(\.be/|be\.com/playlist)\S+', Provider('http://www.youtube.com/oembed?scheme=https&'))

            providers.register('https?://(\S*.)?scribd.com/(doc|document)/\S+(/\S+)?', Provider('http://www.scribd.com/services/oembed'))

            response = providers.request(url)
            html = response.get('html', '')
            html = html.replace('height="%s"' % response.get('height'), '')
            html = html.replace('width="%s"' % response.get('width'), 'style="width:100%; height:100%; position: absolute; top: 0; left: 0"')
            html = mark_safe(render_to_string('core/partials/responsive_embed.html', {'html': html}))

            response.update({
                'html': html
            })

            return JsonResponse(response)

        except Exception as e:
            return JsonResponse({'success': False, 'message': e.message})
