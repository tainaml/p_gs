from django.shortcuts import render_to_response, render


def handler400(request):
    STATUS = 400
    return render(request, "400.html", status=STATUS)


def handler403(request):
    STATUS = 403
    return render(request, "404.html", status=STATUS)


def handler404(request):
    STATUS = 404
    return render(request, "404.html", status=STATUS)


def handler500(request):
    STATUS = 500
    return render(request, "500.html", status=STATUS)
