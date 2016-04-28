from django.utils.translation import ugettext as _
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.views.generic import View

from .service.forms import JobSearchForm
from .service.business import get_job


def do_list(request):
    return render(request, 'job_vacation/index.html')


def job(request):
    return render(request, 'job_vacation/job.html')


class BaseJobView(View):

    template = "job_vacation/index.html"
    form = JobSearchForm

    def do_return_default(self, request, response_data):
        return render(request, self.template, response_data)

    def do_return_ajax(self, request, response_data):
        pass

    def do_return(self, request, response_data):
        if request.is_ajax():
            return self.do_return_ajax(request, response_data)
        return self.do_return_default(request, response_data)


class JobView(BaseJobView):

    def get(self, request):

        form = self.form(request.GET)
        form.set_items_per_page(2)

        jobs = form.process()

        response_data = {
            'jobs': jobs,
            'form': form
        }

        return self.do_return(request, response_data)


class JobListView(JobView):

    template = "job_vacation/partials/results.html"

    def do_return_ajax(self, request, response_data):
        return render(request, self.template, response_data)


class JobDetailView(BaseJobView):

    template = "job_vacation/job.html"

    def get(self, request, job_slug, job_id):

        job = get_job(job_id, job_slug)

        if not job:
            raise Http404(_("Job not found!"))

        response_data = {
            'job': job
        }

        return self.do_return(request, response_data)
