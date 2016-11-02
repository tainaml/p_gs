from apps.core.business import feed as FeedBusiness
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.views.generic import View
from apps.article.models import Article
from apps.core.business.content_types import ContentTypeCached
from apps.feed.models import FeedObject
import micawber
from micawber.providers import Provider


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


        count = count if count and count < 10 else 4

        try:

            related_object = FeedBusiness.get_related_posts_from_item(instance_id, instance_type, post_type, count)

        except Exception, e:
            return self.return_error(request, None)

        context = {
            'feed_records': related_object.get('feed_records'),
            'template_path': related_object.get('template_path')
        }

        return self.return_success(request, context)

class Home(View):

    def get(self, request):

        return render(request, 'home/index.html')


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
