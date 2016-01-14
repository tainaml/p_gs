from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import View

from rede_gsti import settings
from .service import business as Business
from .localexceptions import NotFoundSocialSettings


class SocialActionBaseView(View):

    not_found = Http404(_('SocialAction not Found.'))

    def return_error(self, request, context=None):
        pass

    def return_success(self, request, context=None):
        pass


class SocialActionView(SocialActionBaseView):

    def return_error(self, request, context=None):
        if request.is_ajax():
            if not context:
                context = {}

            _context = context
            return JsonResponse(_context, status=400)

        raise context['not_found']

    def return_success(self, request, context=None):
        if request.is_ajax():
            if not context:
                context = {}

            _context = context
            return JsonResponse(_context, status=200)

        return redirect(context['url_next'])

    @method_decorator(login_required)
    def get(self, request, object_to_link, content, action):

        try:
            Business.act_by_content_type_and_id(request.user, content, object_to_link, action)
            likes = Business.user_likes_by_object_content_type_and_id(
                user=request.user,
                content_type=content, 
                object_id=object_to_link
            )
            unlikes = Business.user_unlikes_by_object_content_type_and_id(
                user=request.user,
                content_type=content, 
                object_id=object_to_link
            )

            i_liked = Business.user_liked_by_id_and_content_type(
                user=request.user,
                content_type=content, 
                object_id=object_to_link
            )
            i_unliked = Business.user_unliked_by_id_and_content_type(
                user=request.user,
                content_type=content, 
                object_id=object_to_link
            )

            if i_liked:
                action_response = settings.SOCIAL_LABELS[settings.SOCIAL_LIKE]
            elif i_unliked:
                action_response = settings.SOCIAL_LABELS[settings.SOCIAL_UNLIKE]
            else:
                action_response = None

        except NotFoundSocialSettings:
            context = {
                'status': 400,
                'msg': _('SocialAction not Found.'),
                'not_found': self.not_found
            }
            return self.return_error(request, context)
        
        context = {
            'status': 200,
            'action_request': action,
            'action_response': action_response,
            'likes': likes,
            'unlikes': unlikes,
            'url_next': request.GET.get('url_next')
        }
        return self.return_success(request, context)


class SocialActionAjax(SocialActionView):

    def return_error(self, request, context=None):
        if not context:
            context = {}

        _context = context

        return JsonResponse(_context, status=400)

    def return_success(self, request, context=None):
        if not context:
            context = {}

        _context = context

        return JsonResponse(_context, status=200)


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


class SocialActionBaseFollowings(SocialActionBaseView):

    template_path = 'socialactions/followings_box.html'

    def get_template(self, template_type=None):
        return self.template_path

    def get_context(self, request, model_obj, list_items):
        return {}


class SocialActionFollowingsViews(SocialActionBaseFollowings):

    def get_template(self, template_type=None):
        if template_type and template_type == "community":
            self.template_path = 'socialactions/communities_box.html'

        return self.template_path

    def get_context(self, request, model_obj, list_items):
        return {
            'items': list_items,
            'content_type': list_items[0].content_type if list_items and list_items[0].content_type else list_items,
            'object': model_obj.author,
            'url_next': request.GET['next'] if 'next' in request.GET else '',
            'page': (list_items.number if list_items and list_items.number else 0) + 1
        }

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

        context = {}
        context.update(self.get_context(request, model_obj, list_followings))

        if model_obj and model_obj.content_type.model:
            self.get_template(model_obj.content_type.model)

        return render(request, self.template_path, context)


class SocialActionSuggestArticleToUser(SocialActionBaseView):

    def return_error(self, request, context=None):
        if request.is_ajax():
            if not context:
                context = {}

            _context = context
            return JsonResponse(_context, status=400)

        raise context['not_found']

    def return_success(self, request, context=None):
        if request.is_ajax():
            if not context:
                context = {}

            _context = context
            return JsonResponse(_context, status=200)

        return redirect(context['url_next'])

    @method_decorator(login_required)
    def post(self, request, object_to_link, content):

        users = request.POST.get('users', [])
        if not users:
            context = {
                'status': 400,
                'errors': {'error_field': [_('No user was selected.')]}
            }
            return self.return_error(request, context)

        try:
            response_suggest = Business.suggest_post(request.user, object_to_link, content, users)
        except NotFoundSocialSettings:
            context = {
                'status': 400,
                'msg': _('SocialAction not Found.'),
                'not_found': self.not_found
            }
            return self.return_error(request, context)

        context = {
            'status': 200,
            'url_next': request.GET.get('url_next')
        }
        return self.return_success(request, context)


class SocialUserActed(View):
    @method_decorator(login_required)
    def get(self, request, object_to_link, content, action):
        try:
            data = {'acted': not not Business.user_acted_by_content_and_object_id(request.user, content, object_to_link, action)}
        except:
            raise Http404()

        return JsonResponse(data)

class SocialActXHR(View):

    @method_decorator(login_required)
    def get(self, request, object_to_link, content, action):

        try:

            action = Business.act_by_content_type_and_id(request.user, content, object_to_link, action)

            return JsonResponse({'acted': not not action})
        except ValueError as e:

            raise Http404()