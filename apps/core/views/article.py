from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from apps.article import views
from apps.comment.models import Comment
from apps.comment.service.forms import CreateCommentForm
from apps.community.models import Community
from apps.feed.models import FeedObject
from ..forms.article import CoreArticleBaseForm, CoreArticleContributorForm
from push_notifications.models import GCMDevice
from apps.core.business import user as UserBusiness
from apps.core.business import article as core_article_business        #self.fields.set('communities')

class CoreArticleEditView(views.ArticleEditView):

    form_article = CoreArticleBaseForm

    def prepare_context(self, request, context):
        context = super(CoreArticleEditView, self).prepare_context(request, context)

        communities = UserBusiness.get_all_communities_list(request.user)

        try:

            first_feed = self.the_article.feed.first()
            if first_feed:
                feed_communities = UserBusiness.get_user_communities_list_from_queryset(
                    self.the_article.feed.all().first().communities.all(),
                    request.user
                )
                communities = communities + feed_communities

        except Exception as e:
            pass

        context.update(communities=communities)

        return context

    def check_user_is_contributor(self, request):
        is_contributor = False

        try:
            is_contributor = request.user.profile.contributor
        except Exception as e:
            pass
        return is_contributor

    @method_decorator(login_required)
    def get(self, request, article_id=None, *args, **kwargs):

        if self.check_user_is_contributor(request):
            self.form_article = CoreArticleContributorForm

        return super(CoreArticleEditView, self).get(request, article_id, *args, **kwargs)

    @method_decorator(login_required)
    def post(self, request, article_id=None, *args, **kwargs):

        if self.check_user_is_contributor(request):
            self.form_article = CoreArticleContributorForm


        return super(CoreArticleEditView, self).post(request, article_id, *args, **kwargs)


class CoreArticlePreView(CoreArticleEditView):

    def prepare_context(self, request, context):

        context.update({
            'isPreview': True
        })

        return super(CoreArticlePreView, self).prepare_context(request, context)

    @method_decorator(login_required)
    def get(self, request, article_id=None, *args, **kwargs):
        self.template_name = 'article/single-preview.html'
        return super(CoreArticlePreView, self).get(request, article_id, *args, **kwargs)


class CoreArticleView(views.ArticleView):

    form_comment = CreateCommentForm

    # @Override
    def filter_article(self, request=None, year=None, month=None, slug=None, prefetch=None):


        article_dict = core_article_business.get_article(year, month, slug, prefetch)

        if not article_dict['article']:
            '''
            Only works when article exists
            '''
            raise self.article_not_found

        if article_dict['article'].status == core_article_business.Article.STATUS_TRASH:
            raise self.article_not_found

        elif article_dict['article'].status == core_article_business.Article.STATUS_DRAFT \
                and article_dict['article'].author != request.user:
            '''
            If the item is Draft status only the author can view
            '''
            raise self.article_not_found

        return article_dict

    def get(self, request, year, month, slug):


        fcm_device = GCMDevice.objects.get(registration_id="token", cloud_message_type="FCM", user=request.user)
        fcm_device.send_message("This is a message")
        prefetch = (
            'content_object__author',
             'content_object__author__profile', 'content_object__author__profile__occupation',
            'content_object__author__profile__occupation__responsibility',
            'content_object__author__profile__occupation',
            'communities',
            'communities__taxonomy'
        )

        article_dict = self.filter_article(request, year, month, slug, prefetch)
        article = article_dict['article']
        has_old_comments = False

        if article:
            has_old_comments = article.old_comments.all().exists()
            if article_dict['redirect']:
                page_format = request.path.split(".")[-1]
                if page_format == 'amp':
                    return redirect('amp:article-single', article.year, article.month, article.slug, permanent=True)
                else:
                    return redirect('article:view', article.year, article.month, article.slug, permanent=True)


        context = {'article': article, 'feed': article_dict['feed'],'has_old_comments': has_old_comments}
        context.update(self.get_context(request, article))

        return render(request, self.template_name, context)

    def get_context(self, request, article_instance=None):

        comments = Comment.objects.filter(
            object_id=article_instance.id
        ).prefetch_related('author', 'author__profile', 'author__profile__occupation')

        return {
            'comments': comments,
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