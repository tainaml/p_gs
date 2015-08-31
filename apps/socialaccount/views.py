from django.shortcuts import render


def index(request):
    """
    Show the index page

    :param request:
    :return: HTML
    """
    return render(request, 'socialaccount/index.html')
