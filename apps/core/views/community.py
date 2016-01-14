from django.http import JsonResponse
from django.shortcuts import render

from apps.community import views
from apps.community.models import Community
from apps.community.service import business as Business
from apps.core.forms.community import CoreCommunityFeedFormSearch, CoreCommunityQuestionFeedFormSearch, \
    CoreCommunitySearchVideosForm, CoreCommunityFollowersForm
from apps.socialactions.service.business import get_users_acted_by_model
from rede_gsti import settings
from apps.core.business import community as BusinessCommunity
from apps.userprofile.service import business as BusinessUserProfile


class CoreCommunityView(views.CommunityView):

    template_path = 'community/community-view.html'

    def get_context(self, request, community_instance=None):

        if request.user and request.user.is_authenticated():

            if isinstance(community_instance, Community):
                community_followers = get_users_acted_by_model(model=community_instance,
                                                               action=settings.SOCIAL_FOLLOW,
                                                               filter_parameters={'author': request.user},
                                                               itens_per_page=20,
                                                               page=1)

                return {'user_follows_community': community_followers}

        return {}


class CoreCommunityFollowersView(CoreCommunityView):

    template_path = 'community/community-followers.html'

    def get_context(self, request, community_instance=None):

        states = BusinessUserProfile.get_states(1)
        return {'states': states}


class CoreCommunityAboutView(CoreCommunityView):

    template_path = 'community/community-about.html'


class CoreCommunitySearch(CoreCommunityView):

    template_path = 'community/community-view.html'

    def get_context(self, request, community_instance=None):
        context = super(CoreCommunitySearch, self).get_context(request, community_instance)
        itens_by_page = 10

        self.form = CoreCommunityFeedFormSearch(
            community_instance,
            ['article', 'question'],
            itens_by_page,
            request.GET
        )
        feed_objects = self.form.process()

        context.update({'feed_objects': feed_objects, 'form': self.form, 'page': self.form.cleaned_data['page'] + 1})

        return context


class CoreCommunityList(CoreCommunitySearch):

    template_path = 'community/partials/community-list.html'

    def get_context(self, request, community_instance=None):
        context = super(CoreCommunityList, self).get_context(request, community_instance)

        return context


class CoreCommunityFeedView(CoreCommunitySearch):

    template_path = 'community/community-view.html'


class CoreCommunityQuestionSearch(CoreCommunityView):

    template_path = 'community/community-questions.html'

    def get_context(self, request, community_instance=None):
        context = super(CoreCommunityQuestionSearch, self).get_context(request, community_instance)
        itens_by_page = 2

        self.form = CoreCommunityQuestionFeedFormSearch(
            community_instance,
            ['question'],
            itens_by_page,
            request.GET
        )
        feed_objects = self.form.process()

        context.update({'feed_objects': feed_objects, 'form': self.form, 'page': self.form.cleaned_data['page'] + 1})

        return context


class CoreCommunityQuestionFeedView(CoreCommunityQuestionSearch):

    template_path = 'community/community-questions.html'


class CoreCommunityQuestionList(CoreCommunityQuestionSearch):

    template_path = 'community/partials/community-question-list.html'

    def get_context(self, request, community_instance=None):
        context = super(CoreCommunityQuestionList, self).get_context(request, community_instance)

        return context


class CoreCommunityVideosSearch(views.CommunityView):

    template_path = "community/community-videos.html"

    form_videos = CoreCommunitySearchVideosForm

    def return_error(self, request, context=None):
        pass

    def return_success(self, request, context=None):
        return render(request, self.template_path, context)

    def get_context(self, request, community_instance=None):

        form = self.form_videos(community_instance, 10, request.GET)

        videos = form.process()

        have_posts = True if hasattr(videos, 'object_list') and videos.object_list else False

        return {
            'feed_objects': videos,
            'have_posts': have_posts,
            'form': form,
            'page': form.cleaned_data.get('page', 1) + 1
        }


class CoreCommunityVideosView(CoreCommunityVideosSearch):
    pass


class CoreCommunityVideosList(CoreCommunityVideosSearch):
    
    template_path = "community/partials/community-videos-list.html"


class CoreCommunityLoad(views.View):

    template_path = ""

    def return_error(self, request, context=None):
        pass

    def return_success(self, request, context=None):
        if not context:
            context = {}

        if request.is_ajax():
            _context = {
                'template': render(request, self.template_path, context).content
            }
            return JsonResponse(_context, status=200)

    def change_template(self, template_path):
        self.template_path = template_path

    def get_context(self, request, *args, **kwargs):
        return {}

    def post(self, request, object_id, content_type):

        url_next = request.POST.get('url-next')

        communities = BusinessCommunity.get_random_communities_by_article_or_question(
            object_id=object_id,
            content_type=content_type
        )

        context = {
            'communities': communities,
            'url_next': url_next
        }
        context.update(self.get_context(request))

        self.change_template("%s/partials/%s-community-list.html" % (content_type, content_type))

        return self.return_success(request, context)


class CoreCommunityFollowersSearch(views.CommunityBaseView):

    template_path = "community/partials/community-followers-list.html"

    form = CoreCommunityFollowersForm

    def return_success(self, request, context=None):
        if request.is_ajax():
            _context = {
                'template': render(request, self.template_path, context).content
            }
            return JsonResponse(_context, status=200)

        return render(request, self.template_path, context)

    def get(self, request):

        form = self.form(False, 6, request.GET)
        followers = form.process()

        context = {
            'followers': followers,
            'form': form,
            'url_next': request.GET.get('next', '')
        }
        context.update(self.get_context(request))

        return self.return_success(request, context)

    def get_context(self, request):
        return {}


class CoreCommunityFollowersSearchList(CoreCommunityFollowersSearch):

    def return_success(self, request, context=None):
        return render(request, self.template_path, context)


class CommunityRelated(CoreCommunityView):

    template_path = "community/partials/community-related.html"

    def get(self, request, community_slug=None):

        communities = BusinessCommunity.get_related_communities(community_slug)

        context = {'communities': communities}

        return JsonResponse({'template':render(request, self.template_path, context).content})


class CommunityCheckUserFollows(views.View):

    def post(self, request):

        community = Business.get_community(request.POST.get('community'))

        if not community:
            return JsonResponse({'msg': 'Community not found!'}, status=400)

        follows_community = get_users_acted_by_model(
            model=community,
            action=settings.SOCIAL_FOLLOW,
            filter_parameters={'author': request.user},
            itens_per_page=5,
            page=1
        )

        follows = True if follows_community else False

        return JsonResponse({'follows': follows}, status=200)