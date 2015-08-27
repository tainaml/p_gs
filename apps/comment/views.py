from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from service.forms import CreateCommentForm
# Create your views here.

def index_teste(request):

    return render(request, 'comment/index_teste.html')

@login_required
@require_POST
def save(request):
    form = CreateCommentForm(request.user, request.POST)

    if not form.process():
        pass

    return redirect('/')