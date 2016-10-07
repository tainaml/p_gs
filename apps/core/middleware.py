import re
from django.shortcuts import redirect
from django.urls import reverse

from django.utils.html import strip_spaces_between_tags
from django.conf import settings

RE_MULTISPACE = re.compile(r"\s{2,}!<pre\s{2,}pre>")
RE_NEWLINE = re.compile(r"\n")
 
class MinifyHTMLMiddleware(object):
    def process_response(self, request, response):
        if 'text/html' in response.get('Content-Type', []) and getattr(settings, 'COMPRESS_HTML', True):
            response.content = strip_spaces_between_tags(response.content.strip())
            response.content = RE_MULTISPACE.sub(" ", response.content)
            response.content = RE_NEWLINE.sub("", response.content)
        return response


class WizardMiddleware(object):

    whitelist = [
        'wizard_proxy_view',
        'LogoutView',
        'index',
        'serve',
    ]

    whitelist_apps = [
        'admin'
    ]

    def __init__(self, get_response=None):
        self.get_response = get_response

    def process_view(self, request, view_func, view_args, view_kwargs):

        if request.resolver_match.app_name in self.whitelist_apps:
            return None

        if view_func.__name__ in self.whitelist:
            return None

        if request.is_ajax():
            return None

        if request.user and hasattr(request.user, "user_profile") \
            and request.user.user_profile.wizard_step + 1 <= int(getattr(settings, 'WIZARD_STEPS_TOTAL')):

            step_to_go = request.user.user_profile.wizard_step + 1

            return redirect(to="profile:wizard", step=step_to_go)

        return None
