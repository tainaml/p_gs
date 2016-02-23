from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator

from apps.article import views
from apps.comment.service.forms import CreateCommentForm
from apps.community.models import Community
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

    form_comment = CreateCommentForm
    def get_context(self, request, article_instance=None):
        feed_object = BusinessFeed.BusinessFeed.get_feed(article_instance)

        return {
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