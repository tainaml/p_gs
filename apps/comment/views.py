from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from service.forms import CreateCommentForm, EditCommentForm
from .models import Comment
# Create your views here.

def index_teste(request):
    return render(request, 'comment/index_teste.html')


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
    if 'next_url' not in request.POST or \
        'comment_id' not in request.POST:
        raise Http404()
    comment = get_object_or_404(Comment, pk=request.POST['comment_id'])

    form = EditCommentForm(request.user, comment, request.POST)

    if not form.process():

        return render(request, 'comment/create.html', {'form': form})

    return redirect(request.POST['next_url'])