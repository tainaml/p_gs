from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views.generic import View
from django_thumbor import generate_url
from django.contrib.auth.decorators import login_required
from django.conf import settings

from apps.core.forms.user import CoreSearchFollowings
from apps.socialactions.service.forms import UserCountForm
from apps.userprofile.service.business import get_user


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
            elif u.content_object.profile and u.content_object.profile.gender:
                img_url = settings.AVATAR[u.content_object.profile.gender]
            else:
                img_url = settings.AVATAR['M']

            thumbnail = generate_url(img_url, width=20, height=20, thumbor_server=settings.THUMBOR_SERVER)

            user = {
                'name': u.content_object.get_full_name(),
                'img': thumbnail,
                'id': u.content_object.id
            }
            users.append(user)

        context = {'users': users}
        return self.return_success(request, context)

class CountActions(View):

    def get(self, request, username, action):

        user = get_user(username)
        if user:
            form_useractions = UserCountForm(user=user, data={'action': action})
            count = form_useractions.process()
            return JsonResponse({'count': count})

        raise Http404()