from django.shortcuts import render
from django.views.generic import View


def do_list(request):
    return render(request, 'job_vacation/index.html')


class JobListSearch(View):

    def get(self, request):
        pass
