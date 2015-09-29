from django.contrib.contenttypes.models import ContentType
from apps.community import views
from apps.community.models import Community
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


class CoreCommunityFeedView(CoreCommunityView):

    template_path = 'community/community-view.html'

    def get_context(self, request, community_instance=None):
        context = super(CoreCommunityFeedView, self).get_context(request, community_instance)

        content_types = ContentType.objects.filter(model__in=['article', 'question'])

        object_taxonomies = FeedObject.objects.filter(
            content_type__in=content_types,
            taxonomies=community_instance.taxonomy
        ).prefetch_related("content_object__author", "content_object__author__profile")

        context.update({'object_taxonomies': object_taxonomies})

        return context


class CoreCommunityQuestionFeedView(CoreCommunityView):

    template_path = 'community/community-view.html'

    def get_context(self, request, community_instance=None):
        content_type = ContentType.objects.get(model='question')

        object_taxonomies = FeedObject.objects.filter(
            content_type=content_type,
            taxonomies=community_instance.taxonomy
        ).order_by(
            "-question__question_date"
        ).prefetch_related(
            "content_object__author",
            "content_object__author__profile"
        )

        return {'object_taxonomies': object_taxonomies}