from apps.community import views
from apps.socialactions.service.business import get_users_acted_by_model
from rede_gsti import settings


class CoreCommunityView(views.CommunityView):

    template_path = 'community/core_view_community.html'

    def get_context(self, request, community_instance=None):
        page = request.GET['p'] if 'p' in request.GET else 1
        community_followers = get_users_acted_by_model(model=community_instance,
                                                       action=settings.SOCIAL_FOLLOW,
                                                       itens_per_page=9,
                                                       page=page)

        return {
            'community_followers': community_followers,
            'page': (community_followers.number if community_followers and community_followers.number else 0) + 1
        }


class CoreCommunityFollowersView(CoreCommunityView):

    template_path = 'community/core_view_followers.html'