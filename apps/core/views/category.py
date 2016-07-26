from django.http import Http404
from django.shortcuts import render
from django.views.generic import View
from django.utils.translation import gettext
from apps.community.models import Community
from apps.core.forms.category import ListArticleCommunityForm
from apps.custom_base.views import FormBaseListView

from apps.taxonomy.models import Taxonomy


class CoreCategoryPageView(View):

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

    def get(self, request, category_slug):

        try:

            self.category = Taxonomy.objects.get(slug=category_slug, term__slug='categoria')
            self.category.community_related = Community.objects.get(slug=category_slug, taxonomy__term__slug='categoria')
        except Taxonomy.DoesNotExist:
            raise Http404(gettext('Category not found or not root category.'))

        self.get_context().update({
            'category': self.category,
            'category_slug': category_slug
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
        self.context.update({'communities': self.process_return, 'category_id': request.GET['category_id']})






