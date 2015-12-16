from django import http
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import View
from ..business import feed as Business

class FeedContentOfficial(View):

    @method_decorator(login_required)
    def get(self, request, content_type, object_id):

        if not request.user.profile.isContributor():
            raise PermissionDenied

        if not request.GET.get('next'):
            raise http.Http404()

        Business.toggle_feed_official(content_type, object_id)

        return redirect(request.GET.get('next'))