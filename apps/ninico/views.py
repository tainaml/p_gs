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