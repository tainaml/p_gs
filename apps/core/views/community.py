from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from apps.community import views
from apps.community.models import Community
from apps.socialactions.service.business import get_users_acted_by_model
from apps.taxonomy.models import ObjectTaxonomy
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

    def get_context(self, request, community_instance=None):
        context = super(CoreCommunityFeedView, self).get_context(request, community_instance)
        community_object_taxonomies = Business.get_taxonomies_by_model(community_instance)
        taxonomies = [object_taxonomy.taxonomy for object_taxonomy in community_object_taxonomies]

        content_types = ContentType.objects.filter(model__in=['article', 'question'])

        object_taxonomies = ObjectTaxonomy.objects.filter(
            Q(taxonomy__in=taxonomies) &
            Q(content_type__in=content_types)

        ).distinct("object_id", "content_type", "reverse_object__relevance") \
            .order_by("-reverse_object__relevance")


        context.update({'object_taxonomies': object_taxonomies})

        return context

    template_path = 'community/community-view.html'

