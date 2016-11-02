from django.shortcuts import render


def test_async(request):
    return render(request, 'mailmanager/test_async.html')


def send_async(request):
    return render(request, 'mailmanager/test_async.html')