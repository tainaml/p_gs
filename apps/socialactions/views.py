from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils import timezone
from rede_gsti import settings
from .service import business as Business
from .localexceptions import NotFoundSocialSettings


@login_required
def act(request, object_to_link, content, action):

    try:
        Business.act_by_content_type_and_id(request.user, content, object_to_link, action)

    except NotFoundSocialSettings:
        raise Http404()

    return redirect(request.GET['url_next'])


def followers(request, content_type_id, object_filter_id):

    page = request.GET['p'] if 'p' in request.GET else 1

    try:
        model_obj = Business.get_content_object_by_id_and_content_type_id_and_action_id(content_type=content_type_id,
                                                                                        object_id=object_filter_id,
                                                                                        action_type=settings.SOCIAL_FOLLOW)

        list_followers = Business.get_users_acted_by_model(model=model_obj.content_object,
                                                           action=settings.SOCIAL_FOLLOW,
                                                           itens_per_page=10,
                                                           page=page)
    except ValueError:
        raise Http404()

    context = {
        'followers': list_followers,
        'content_type': list_followers[0].content_type if list_followers and list_followers[0].content_type else None,
        'object': model_obj.content_object,
        'url_next': request.GET['next'] if 'next' in request.GET else '',
        'page': (list_followers.number if list_followers and list_followers.number else 0) + 1
    }

    return render(request, 'socialactions/followers_partial_list.html', context)