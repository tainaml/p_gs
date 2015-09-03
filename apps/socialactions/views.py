from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect
from django.utils import timezone
from .service import business as Business
from .localexceptions import NotFoundSocialSettings
# Create your views here.


@login_required
def act(request, object_to_link, content, action):

    try:
        Business.act_by_content_type_and_id(request.user, content, object_to_link, action)

    except NotFoundSocialSettings:
        raise Http404()


    return redirect(request.GET['url_next'])

