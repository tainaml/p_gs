from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from service.forms import CreateCommentForm
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