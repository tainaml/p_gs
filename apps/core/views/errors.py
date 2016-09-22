from django.shortcuts import render_to_response, render


def handler400(request):
    return render(request, "400.html")


def handler403(request):
    response = render_to_response('404.html')
    return render(request, "404.html")


def handler404(request):
    return render(request, "404.html")


def handler500(request):
    return render(request, "500.html")
