from django.utils.decorators import method_decorator
from django.views.generic import View
from django.shortcuts import render
from apps.core.business import socialactions as Business
from apps.socialactions.localexceptions import NotFoundSocialSettings
from django.contrib.auth.decorators import login_required
from apps.userprofile.service.business import get_user


class SocialActionSeeLater(View):
    template_path = 'socialactions/see-later.html'

    @method_decorator(login_required)
    def get(self, request, username):

        criteria = None
        user = get_user(username)
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
            'criteria':self.template_path
        }

        return render(request, self.template_path, context)


class SocialActionRemoveSeeLater(View):
    template_path = 'socialactions/see-later.html'

    @method_decorator(login_required)
    def post(self, request, username):

        itens_to_remove = request.POST.getlist(u'itens_to_remove[]')
        user = get_user(username)

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
            'page': (content.number if content and content.number else 0) + 1,
            'criteria':self.template_path
        }

        return render(request, self.template_path)


class SocialActionFavourite(View):
    template_path = 'socialactions/favourite.html'

    @method_decorator(login_required)
    def get(self, request, username):

        criteria = None
        user = get_user(username)
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
                'criteria':self.template_path
            }
            return self.return_error(request, context)

        context = {
            'articles': content,
            'url_next': request.GET['next'] if 'next' in request.GET else '',
            'page': (content.number if content and content.number else 0) + 1,
            'criteria':self.template_path
        }

        return render(request, self.template_path, context)


class SocialActionRemoveFavourite(View):
    template_path = 'socialactions/favourite.html'

    @method_decorator(login_required)
    def post(self, request, username):

        itens_to_remove = request.POST.getlist(u'itens_to_remove[]')
        user = get_user(username)

        try:
            content = Business.remove_favourite_content(user=user, itens_to_remove=itens_to_remove)

        except NotFoundSocialSettings:
            context = {
                'status': 400,
                'msg': _('SocialAction not Found.'),
                'not_found': self.not_found,
                'url_next': request.GET['next'] if 'next' in request.GET else '',
                'page': (itens_to_remove.number if itens_to_remove and itens_to_remove.number else 0) + 1,
                'criteria':self.template_path
            }
            return self.return_error(request, context)

        context = {
            'articles': content,
            'url_next': request.GET['next'] if 'next' in request.GET else '',
            'page': (itens_to_remove.number if itens_to_remove and itens_to_remove.number else 0) + 1,
            'criteria':self.template_path
        }

        return render(request, self.template_path, context)


class SocialActionSuggest(View):
    template_path = 'socialactions/suggest.html'

    @method_decorator(login_required)
    def get(self, request, username):

        criteria = None
        user = get_user(username)
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
                'criteria':self.template_path
            }
            return self.return_error(request, context)

        context = {
            'articles': content,
            'url_next': request.GET['next'] if 'next' in request.GET else '',
            'page': (content.number if content and content.number else 0) + 1,
            'criteria':self.template_path
        }

        return render(request, self.template_path, context)


class SocialActionRemoveSuggest(View):
    template_path = 'socialactions/partials/suggest.html'

    @method_decorator(login_required)
    def post(self, request, username):

        itens_to_remove = request.POST.getlist(u'itens_to_remove[]')
        user = get_user(username)

        try:
            content = Business.remove_suggest_content(user=user, itens_to_remove=itens_to_remove)

        except NotFoundSocialSettings:
            context = {
                'status': 400,
                'msg': _('SocialAction not Found.'),
                'not_found': self.not_found,
                'url_next': request.GET['next'] if 'next' in request.GET else '',
                'page': (len(itens_to_remove) if len(itens_to_remove) and len(itens_to_remove) else 0) + 1,
                'criteria': self.template_path
            }
            return self.return_error(request, context)

        context = {
            'articles': content,
            'url_next': request.POST['next'] if 'next' in request.POST else '',
            'page': (len(itens_to_remove) if itens_to_remove and len(itens_to_remove) else 0) + 1,
            'criteria': self.template_path
        }

        return render(request, self.template_path, context)