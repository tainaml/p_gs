from django.shortcuts import render

from apps.mailmanager.tasks import send_mail_async


def test_async(request):
    return render(request, 'mailmanager/test_async.html')


def send_async(request):
    send_mail_async.delay()
    return render(request, 'mailmanager/test_async.html')