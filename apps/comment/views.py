from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.views.decorators.http import require_POST, require_GET
from service.forms import CreateCommentForm, EditCommentForm
from .service import business as Business


def index_teste(request):
    user = User.objects.all()[0]
    return render(request, 'comment/index_teste.html', {'user': user})


@login_required
@require_POST
def save(request):
    if 'content_object_id' not in request.POST \
            or 'content_type' not in request.POST \
            or 'next_url' not in request.POST:
        raise Http404()

    form = CreateCommentForm(request.user, request.POST)

    if not form.process():
        return render(request, 'comment/create.html', {'form': form})

    return redirect(request.POST['next_url'])


@login_required
@require_POST
def update(request):
    if 'next_url' not in request.POST or 'comment_id' not in request.POST:
        raise Http404()

    form = EditCommentForm(request.user, request.POST['comment_id'], request.POST)

    if not form.process():
        return render(request, 'comment/create.html', {'form': form})

    return redirect(request.POST['next_url'])


@login_required
@require_GET
def delete(request, id):

    comment = Business.retrieve_own_comment(comment_id=id, user=request.user)
    if comment:
        Business.delete_comment(comment)
    else:
        raise Http404()

    return redirect('/comment/index_teste')