from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect
from django.utils import timezone
from .service import business as Business
# Create your views here.


@login_required
def like(request, object_to_link, content, action):

    try:


        i_liked = UserAction.objects.filter(content_type=model_type,
                                            author=request.user,
                                            object_id=object_to_link,
                                            action_type=ActionType.LIKE)[0]


        try:
            i_unliked = UserAction.objects.filter(content_type=model_type,
                                                author=request.user,
                                                object_id=object_to_link,
                                                action_type=ActionType.UNLIKE)[0]
        except:
            i_unliked = None

        if i_liked and i_liked.action_type:
            i_liked.delete()
            if action_type == ActionType.LIKE:
                return redirect(request.GET['url_next'])

        if i_unliked and i_unliked.action_type:
            i_unliked.delete()
            if action_type == ActionType.UNLIKE:
                return redirect(request.GET['url_next'])

        action = UserAction(
            author=request.user,
            action_date=timezone.now(),
            action_type=action_type,
            content_object=object_attach
        )

        action.save()
    except ValueError:
        raise Http404()


    return redirect(request.GET['url_next'])