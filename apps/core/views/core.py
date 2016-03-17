from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import View

from apps.article.models import Article
from apps.feed.models import FeedObject


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

    def post(self, request, instance_id, instance_type, post_type=None, count=None):


        count = count if count and count < 10 else 4

        try:
            content_type = ContentType.objects.get(model=instance_type)
            content_object = content_type.get_object_for_this_type(id=instance_id)

            post_type = ContentType.objects.get(model=post_type) if post_type else content_type

            template_path = 'core/partials/related-posts/%s-base.html' % post_type.model

            feed_obj = FeedObject.objects.get(content_type=content_type, object_id=content_object.id)

            feed_records = FeedObject.objects.filter(
                Q(communities__in=feed_obj.communities.all()) &
                Q(content_type=post_type) &
                (
                    (
                        Q(article__status=Article.STATUS_PUBLISH) &
                        Q(article__publishin__lte=timezone.now())
                    )
                )
            ).exclude(
                Q(object_id=content_object.id)
            ).order_by(
                "-date"
            ).distinct(
                "date",
                "object_id",
                "content_type_id"
            )[:count]

        except Exception, e:
            return self.return_error(request, None)

        context = {
            'feed_records': feed_records,
            'template_path': template_path
        }

        return self.return_success(request, context)

class About(View):

    def get(self, request):
        return render(request, 'about.html')


