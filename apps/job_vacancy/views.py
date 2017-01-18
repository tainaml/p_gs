from django.urls import reverse
from django.utils.translation import ugettext as _
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import View
from .service.forms import JobSearchForm
from .service.business import get_job
from apps.job_vacancy.service.editforms import (
    JobVacancyForm
)


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
        form.set_items_per_page(10)

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


class JobEditView(View):

    job = None
    template_name = 'job_vacation/register.html'
    form = None
    form_class = JobVacancyForm

    def get_context(self, request):
        if request.method == 'GET':
            self.form.responsibility_formset = self.form.responsibility_formset(instance=self.job)
            self.form.salary_formset = self.form.salary_formset(instance=self.job)

        return {
            'form': self.form,
        }

    def get(self, request, job_id=None):

        if job_id:
            self.job = get_job(job_id)

        self.form = self.form_class(
            instance=self.job
        )

        return render(

            request,
            template_name=self.template_name,
            context=self.get_context(request)
        )

    def post(self, request, job_id=None):

        if job_id:
            self.job = get_job(job_id)

        self.form = self.form_class(
            data=request.POST,
            instance=self.job
        )

        self.form.responsibility_formset = self.form.responsibility_formset(request.POST, instance=self.form.instance)
        self.form.salary_formset = self.form.salary_formset(request.POST, instance=self.form.instance)
        context = self.get_context(request)

        if self.form.is_valid() and self.form.responsibility_formset.is_valid() and self.form.salary_formset.is_valid():
            self.form.set_author(request.user)
            self.form.save()
            self.form.responsibility_formset.save()
            self.form.salary_formset.save()

            return redirect(reverse("jobs:edit", args=[self.form.instance.id]))
        else:
            context.update({
                'error_message': 'Not saved. Model error.'
            })

        return render(
            request,
            template_name=self.template_name,
            context=context
        )
