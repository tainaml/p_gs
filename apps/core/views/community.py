from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from apps.community import views
from apps.community.models import Community
from apps.core.forms.community import CoreCommunityFeedFormSearch, CoreCommunityQuestionFeedFormSearch
from apps.feed.models import FeedObject
from apps.socialactions.service.business import get_users_acted_by_model
from rede_gsti import settings
from apps.taxonomy.service import business as Business

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