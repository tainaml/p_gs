from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.shortcuts import render
from django_thumbor import generate_url
from apps.core.business import socialactions as Business
from apps.core.forms.user import CoreSearchFollowings
from apps.socialactions.localexceptions import NotFoundSocialSettings
from django.contrib.auth.decorators import login_required
from apps.userprofile.service.business import get_user
from apps.userprofile.service import business as ProfileBusiness
from rede_gsti import settings
from django.utils.translation import gettext as _


class SocialActionSeeLater(View):
    template_path = 'socialactions/see-later.html'

    @method_decorator(login_required)
    def get(self, request, username):

        criteria = None
        user = get_user(username)
        profile = ProfileBusiness.get_profile(user)
        if 'criteria' in request.GET:
            criteria = str(request.GET['criteria'])
            self.template_path = 'socialactions/partials/see-later.html'

        try:
            content = Business.get_see_later_content(user, criteria)

        except NotFoundSocialSettings:
            context = {
                'status': 400,
                'msg': _('SocialAction not Found.'),
                'not_found': self.not_found
            }
            return self.return_error(request, context)

        context = {
            'articles': content,
            'url_next': request.GET['next'] if 'next' in request.GET else '',
            'page': (content.number if content and content.number else 0) + 1,
            'criteria': self.template_path,
            'profile': profile
        }

        return render(request, self.template_path, context)


class SocialActionRemoveSeeLater(View):
    template_path = 'socialactions/see-later.html'

    @method_decorator(login_required)
    def post(self, request, username):

        itens_to_remove = request.POST.getlist(u'itens_to_remove[]')
        user = get_user(username)
        profile = ProfileBusiness.get_profile(user)
        try:
            content = Business.remove_see_later_content(user=user, itens_to_remove=itens_to_remove)

        except NotFoundSocialSettings:
            context = {
                'status': 400,
                'msg': _('SocialAction not Found.'),
                'not_found': self.not_found
            }
            return self.return_error(request, context)

        context = {
            'articles': content,
            'url_next': request.GET['next'] if 'next' in request.GET else '',
            'page': (content.page if content.page and content.page else 0) + 1,
            'criteria': self.template_path,
            'profile': profile
        }

        return render(request, self.template_path)


class SocialActionFavourite(View):
    template_path = 'socialactions/favourite.html'

    @method_decorator(login_required)
    def get(self, request, username):

        criteria = None
        user = get_user(username)
        profile = ProfileBusiness.get_profile(user)
        if 'criteria' in request.GET:
            criteria = str(request.GET['criteria'])
            self.template_path = 'socialactions/partials/favourite.html'

        try:
            content = Business.get_favourite_content(user, criteria)

        except NotFoundSocialSettings:
            context = {
                'status': 400,
                'msg': _('SocialAction not Found.'),
                'not_found': self.not_found,
                'url_next': request.GET['next'] if 'next' in request.GET else '',
                'page': (content.number if content and content.number else 0) + 1,
                'criteria': self.template_path
            }
            return self.return_error(request, context)

        context = {
            'articles': content,
            'url_next': request.GET['next'] if 'next' in request.GET else '',
            'page': (content.number if content and content.number else 0) + 1,
            'criteria': self.template_path,
            'profile': profile
        }

        return render(request, self.template_path, context)


class SocialActionRemoveFavourite(View):
    template_path = 'socialactions/favourite.html'

    @method_decorator(login_required)
    def post(self, request, username):

        itens_to_remove = request.POST.getlist(u'itens_to_remove[]')
        user = get_user(username)
        profile = ProfileBusiness.get_profile(user)
        try:
            content = Business.remove_favourite_content(user=user, itens_to_remove=itens_to_remove)

        except NotFoundSocialSettings:
            context = {
                'status': 400,
                'msg': _('SocialAction not Found.'),
                'not_found': self.not_found,
                'url_next': request.GET['next'] if 'next' in request.GET else '',
                'page': (itens_to_remove.number if itens_to_remove and itens_to_remove.number else 0) + 1,
                'criteria': self.template_path
            }
            return self.return_error(request, context)

        context = {
            'articles': content,
            'url_next': request.GET['next'] if 'next' in request.GET else '',
            'page': (itens_to_remove.page if itens_to_remove and itens_to_remove.page else 0) + 1,
            'criteria': self.template_path,
            'profile': profile
        }

        return render(request, self.template_path, context)


class SocialActionSuggest(View):
    template_path = 'socialactions/suggest.html'

    @method_decorator(login_required)
    def get(self, request, username):

        criteria = None
        user = get_user(username)
        profile = ProfileBusiness.get_profile(user)
        if 'criteria' in request.GET:
            criteria = str(request.GET['criteria'])
            self.template_path = 'socialactions/partials/suggest.html'

        try:
            content = Business.get_suggest_content(user, criteria)

        except NotFoundSocialSettings:
            context = {
                'status': 400,
                'msg': _('SocialAction not Found.'),
                'not_found': self.not_found,
                'url_next': request.GET['next'] if 'next' in request.GET else '',
                'page': (content.number if content and content.number else 0) + 1,
                'criteria': self.template_path
            }
            return self.return_error(request, context)

        context = {
            'articles': content,
            'url_next': request.GET['next'] if 'next' in request.GET else '',
            'page': (content.number if content and content.number else 0) + 1,
            'criteria': self.template_path,
            'profile': profile
        }

        return render(request, self.template_path, context)


class SocialActionRemoveSuggest(View):
    template_path = 'socialactions/partials/suggest.html'

    @method_decorator(login_required)
    def post(self, request, username):

        itens_to_remove = request.POST.getlist(u'itens_to_remove[]')
        user = get_user(username)
        profile = ProfileBusiness.get_profile(user)
        try:
            content = Business.remove_suggest_content(user=user, itens_to_remove=itens_to_remove)

        except NotFoundSocialSettings:
            context = {
                'status': 400,
                'msg': _('SocialAction not Found.'),
                'not_found': self.not_found,
                'url_next': request.GET['next'] if 'next' in request.GET else '',
                'page': (itens_to_remove.page if itens_to_remove and itens_to_remove.page else 0) + 1,
                'criteria': self.template_path
            }
            return self.return_error(request, context)

        context = {
            'articles': content,
            'url_next': request.POST['next'] if 'next' in request.POST else '',
            'page': (itens_to_remove.page if itens_to_remove and itens_to_remove.page else 0) + 1,
            'criteria': self.template_path,
            'profile': profile
        }

        return render(request, self.template_path, context)


class SocialActionFilterFollowings(View):

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

    @method_decorator(login_required)
    def get(self, request):

        form = CoreSearchFollowings(request.user, None, request.GET)
        users_followings = form.process()
        users_followings = users_followings.get('items')

        users = []

        for u in users_followings:
            img_url = u.content_object.profile.profile_picture
            if img_url:
                img_url = str(settings.THUMBOR_MEDIA_URL) + '/' + str(img_url)
                thumbnail = generate_url(img_url, width=20, height=20, thumbor_server=settings.THUMBOR_SERVER)
            else:
                initials = "%s%s" % (u.content_object.first_name[:0] if u.content_object.first_name else '',
                                     u.content_object.last_name[:0] if u.content_object.first_name else '')
                thumbnail = "http://placehold.it/20?text=%s" % initials
            user = {
                'name': u.content_object.get_full_name(),
                'img': thumbnail,
                'id': u.content_object.id
            }
            users.append(user)

        context = {'users': users}
        return self.return_success(request, context)