from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import View
from rede_gsti import settings
from .service import business as Business
from .localexceptions import NotFoundSocialSettings


class SocialActionBaseView(View):

    not_found = Http404(_('SocialAction not Found.'))


class SocialActionView(SocialActionBaseView):

    @method_decorator(login_required)
    def get(self, request, object_to_link, content, action):

        try:
            Business.act_by_content_type_and_id(request.user, content, object_to_link, action)

        except NotFoundSocialSettings:
            raise self.not_found

        return redirect(request.GET['url_next'])


class SocialActionFollowersViews(SocialActionBaseView):

    template_path = 'socialactions/followers_box.html'

    def get(self, request, content_type_id, object_filter_id):
        page = request.GET['p'] if 'p' in request.GET else 1

        try:
            model_obj = Business.get_user_by_params({'content_type': content_type_id,
                                                     'object_id': object_filter_id,
                                                     'action_type': settings.SOCIAL_FOLLOW})

            list_followers = Business.get_users_acted_by_model(model=model_obj.content_object,
                                                               action=settings.SOCIAL_FOLLOW,
                                                               itens_per_page=9,
                                                               page=page)
        except ValueError:
            raise self.not_found

        context = {
            'followers': list_followers,
            'content_type': list_followers[0].content_type if list_followers and list_followers[0].content_type else None,
            'object': model_obj.content_object,
            'url_next': request.GET['next'] if 'next' in request.GET else '',
            'page': (list_followers.number if list_followers and list_followers.number else 0) + 1
        }

        return render(request, self.template_path, context)


class SocialActionFollowingsViews(SocialActionBaseView):

    template_path = 'socialactions/followings_box.html'

    def get(self, request, content_type_id, object_filter_id):
        page = request.GET['p'] if 'p' in request.GET else 1

        try:
            model_obj = Business.get_user_by_params({'content_type': content_type_id,
                                                     'author': object_filter_id,
                                                     'action_type': settings.SOCIAL_FOLLOW})

            list_followings = Business.get_users_acted_by_author(author=model_obj.author,
                                                                 content_type=model_obj.content_type.model,
                                                                 action=settings.SOCIAL_FOLLOW,
                                                                 items_per_page=9,
                                                                 page=page)
        except ValueError:
            raise Http404()

        context = {
            'followings': list_followings,
            'content_type': list_followings[0].content_type if list_followings and list_followings[0].content_type else None,
            'object': model_obj.author,
            'url_next': request.GET['next'] if 'next' in request.GET else '',
            'page': (list_followings.number if list_followings and list_followings.number else 0) + 1
        }

        return render(request, self.template_path, context)