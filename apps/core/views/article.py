from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from apps.article import views
from apps.comment.models import Comment
from apps.comment.service.forms import CreateCommentForm
from apps.community.models import Community
from ..forms.article import CoreArticleForm
from ..business import feed as BusinessFeed
from apps.core.business import user as UserBusiness
from apps.core.business import article as core_article_business

class CoreArticleEditView(views.ArticleEditView):

    form_article = CoreArticleForm

    def prepare_context(self, request, context):
        context = super(CoreArticleEditView, self).prepare_context(request, context)
        communities = UserBusiness.get_user_communities_list(request.user)

        context.update(communities=communities)

        return context


class CoreArticleView(views.ArticleView):

    form_comment = CreateCommentForm

    # @Override
    def filter_article(self, request=None, year=None, month=None, slug=None):
        article_dict = core_article_business.get_article(year, month, slug)

        if not article_dict['article']:
            '''
            Only works when article exists
            '''
            raise self.article_not_found

        if article_dict['article'].status == core_article_business.Article.STATUS_DRAFT \
                and article_dict['article'].author != request.user:
            '''
            If the item is Draft status only the author can view
            '''
            raise self.article_not_found

        return article_dict

    def get(self, request, year, month, slug):
        article_dict = self.filter_article(request, year, month, slug)
        article = article_dict['article']

        if article:
            if article_dict['redirect']:
                return redirect('article:view', article.year, article.month, article.slug, permanent=True)

        context = {'article': article}
        context.update(self.get_context(request, article))

        return render(request, self.template_name, context)

    def get_context(self, request, article_instance=None):

        feed_object = BusinessFeed.BusinessFeed.get_feed(article_instance)
        comments = Comment.objects.filter(object_id=article_instance.id)
        return {
            'comments': comments,
            'feed': feed_object,
            'form_comment': self.form_comment()
        }


class CoreArticleInCommunityView(CoreArticleEditView):

    article_community = False

    @method_decorator(login_required)
    def get(self, request, community_slug=None, *args, **kwargs):

        try:
            self.article_community = Community.objects.get(slug=community_slug)
        except Community.DoesNotExist, e:
            raise Http404(_('Community not Found'))

        # raize 403 if user not follow this community
        if self.article_community:
            user_communities = UserBusiness.get_user_communities(request.user)
            if self.article_community not in user_communities:
                raise PermissionDenied(_('User need follow this community'))

        return super(CoreArticleInCommunityView, self).get(request, article_id=None, *args, **kwargs)

    def prepare_initial_data(self, initial):
        initial.update(communities=[self.article_community])
        return initial

    def prepare_context(self, request, context):

        context = super(CoreArticleInCommunityView, self).prepare_context(request, context)

        form_article = context.get('form_article', None)

        if form_article and 'communities' in form_article.fields:
            form_article.fields["communities"].initial = self.article_community
            context.update(form_article=form_article)

        return context