from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import View
from django.utils.translation import gettext as _

from .service import business as Business


def community_show(request, community_slug):
    return HttpResponse(community_slug)


class CommunityBaseView(View):

    community_not_found = Http404(_('Community not Found.'))

    def filter_community(self, request, community_slug=None):
        community = Business.get_community(slug=community_slug)

        if not community:
            '''
            Only works when community exists
            '''
            raise self.community_not_found

        return community


class CommunityView(CommunityBaseView):

    template_path = 'community/view_community.html'

    def get(self, request, community_slug):

        community = self.filter_community(request, community_slug)
        if not community:
            return self.community_not_found

        return render(request, self.template_path, {'community': community})