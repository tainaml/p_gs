import re
from django.shortcuts import redirect
from django.urls import reverse

from django.utils.html import strip_spaces_between_tags
from django.conf import settings

RE_MULTISPACE = re.compile(r"\s{2,}!<pre\s{2,}pre>")
RE_NEWLINE = re.compile(r"\n")
 
class MinifyHTMLMiddleware(object):
    def process_response(self, request, response):
        if 'text/html' in response['Content-Type'] and getattr(settings, 'COMPRESS_HTML', True):
            response.content = strip_spaces_between_tags(response.content.strip())
            response.content = RE_MULTISPACE.sub(" ", response.content)
            response.content = RE_NEWLINE.sub("", response.content)
        return response

REVERSE_TO_REDIRECT = [
    reverse("profile:wizard", args=[0]),
    reverse("profile:wizard", args=[1]),
    reverse("profile:wizard", args=[2]),
    reverse("profile:wizard", args=[3])

]

class WizardMiddleware(object):

    def __init__(self, get_response=None):
        self.get_response = get_response

    def process_request(self, request):
        if request.user and hasattr(request.user, "user_profile") \
                and request.user.user_profile.wizard_step < settings.WIZARD_STEPS_TOTAL \
                and request.path not in REVERSE_TO_REDIRECT:

            return redirect(to="profile:wizard", step=request.user.user_profile.wizard_step)