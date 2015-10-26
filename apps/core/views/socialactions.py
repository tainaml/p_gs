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

        user = get_user(username)

        try:
            content = Business.get_see_later_content(user)

        except NotFoundSocialSettings:
            context = {
                'status': 400,
                'msg': _('SocialAction not Found.'),
                'not_found': self.not_found
            }
            return self.return_error(request, context)

        context = {
            'articles': content,
        }

        return render(request, self.template_path, context)


class SocialActionRemoveSeeLater(View):
    template_path = 'socialactions/see-later.html'

    @method_decorator(login_required)
    def post(self, request, username):

        itens_to_remove = request.POST.getlist(u'itens_to_remove[]')
        user = get_user(username)

        try:
            Business.remove_see_later_content(user=user, itens_to_remove=itens_to_remove)

        except NotFoundSocialSettings:
            context = {
                'status': 400,
                'msg': _('SocialAction not Found.'),
                'not_found': self.not_found
            }
            return self.return_error(request, context)

        return render(request, self.template_path)