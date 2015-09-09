from django.shortcuts import render

# Create your views here.
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