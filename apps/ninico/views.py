import json
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import HttpResponse


def index(request):
    return render(request, 'home/index.html')

def perfil(request):
    return render(request, 'home/perfil.html')

def feed(request):
    return render(request, 'home/perfil-feed.html')

def about(request):
    return render(request, 'home/perfil-sobre.html')

def relationship(request):
    return render(request, 'home/perfil-relacionamentos.html')

def videos(request):
    return render(request, 'home/perfil-videos.html')

def communities(request):
    return render(request, 'home/perfil-comunidades.html')

def community(request):
    return render(request, 'home/comunidade.html')

def community_about(request):
    return render(request, 'home/comunidade-sobre.html')

def community_question(request):
    return render(request, 'home/comunidade-perguntas.html')

def community_videos(request):
    return render(request, 'home/comunidade-videos.html')

def community_members(request):
    return render(request, 'home/comunidade-membros.html')

def suggestions(request):
    return render(request, 'home/sugestoes.html')

def see_after(request):
    return render(request, 'home/ver-depois.html')

def favorites(request):
    return render(request, 'home/favoritos.html')

def write_article(request):
    return render(request, 'home/criar-artigo.html')

def write_question(request):
    return render(request, 'home/criar-pergunta.html')

def post(request):
    return render(request, 'home/post.html')

def question(request):
    return render(request, 'home/question.html')

def notifications(request):
    return render(request, 'home/notificacoes.html')

def member_notifications(request):
    return render(request, 'home/notificacoes-membros.html')

def questions_and_answers_notifications(request):
    return render(request, 'home/notificacoes-perguntas-e-respostas.html')

def search(request):
    return render(request, 'home/search-result.html')

def category(request):
    return render(request, 'home/categoria.html')


@require_POST
def test_abc(request):

    response_data = {
        'post': request.POST,
        'get': request.GET,
        'files': len(request.FILES),
    }

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def edit_publications(request):
    return render(request, 'home/editar-publicacoes.html')