from django.shortcuts import render


# Create your views here.
def do_list(request):
    return render(request, 'job_vacation/index.html')


def job(request):
    return render(request, 'job_vacation/job.html')