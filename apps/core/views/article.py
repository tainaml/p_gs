import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from apps.article import views
from apps.community.models import Community
from apps.taxonomy.models import Taxonomy
from ..forms.article import CoreArticleForm
from ..business import feed as BusinessFeed
from apps.core.business import user as UserBusiness

class CoreArticleEditView(views.ArticleEditView):

    form_article = CoreArticleForm

    def prepare_context(self, request, context):
        context = super(CoreArticleEditView, self).prepare_context(request, context)
        communities = UserBusiness.get_user_communities_list(request.user)

        context.update(communities=communities)

        return context


class CoreArticleView(views.ArticleView):

    def get_context(self, request, article_instance=None):
        feed_object = BusinessFeed.BusinessFeed.get_feed(article_instance)
        return {
            'feed': feed_object
        }

class CoreArticleInCommunityView(CoreArticleEditView):

    article_community = False

    @method_decorator(login_required)
    def get(self, request, community_slug=None, *args, **kwargs):

        try:
            self.article_community = Community.objects.filter(slug=community_slug)
        except Community.DoesNotExist, e:
            pass

        return super(CoreArticleEditView, self).get(request, article_id=None, *args, **kwargs)

    def prepare_initial_data(self, initial):
        initial.update(communities=self.article_community)
        return initial

    def prepare_context(self, request, context):

        context = super(CoreArticleInCommunityView, self).prepare_context(request, context)

        form_article = context.get('form_article', None)

        if form_article and 'communities' in form_article.fields:
            form_article.fields["communities"].initial = self.article_community
            context.update(form_article=form_article)

        return context