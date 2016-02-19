from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.utils.translation import ugettext as _

from apps.contact.service import business as Business
from apps.contact.service.forms import ContactForm, ContactFormNoAuthenticated


class ContactView(View):

    template_path = "contact/contact.html"

    form = ContactForm

    def return_success(self, request, context=None):
        if request.is_ajax():
            return JsonResponse({
                'template': render(request, self.template_path, context).content
            })
        return render(request, self.template_path, context)

    def get(self, request):

        subjects = Business.get_contact_subjects()
        return self.return_success(request, {'subjects': subjects})


class ContactSaveViews(View):

    template_path = "contact/contact.html"
    form = ContactForm

    def return_error(self, request, context=None):
        subjects = Business.get_contact_subjects()
        context.update({'subjects': subjects})

        if request.is_ajax():
            return JsonResponse({
                'template': render(request, self.template_path, context).content
            })

        messages.add_message(request, messages.SUCCESS, context.get('message'), 'contact')
        return render(request, self.template_path, context)

    def return_success(self, request, context=None):
        if request.is_ajax():
            return JsonResponse({
                'template': render(request, self.template_path, context).content
            })

        messages.add_message(request, messages.SUCCESS, context.get('message'), 'contact')
        return redirect(reverse('contact:create'))

    def post(self, request):

        if not request.user.is_authenticated():
            self.form = ContactFormNoAuthenticated

        form = self.form(request.user, request.POST)
        context = {}

        if form.process():
            return self.return_success(request, {'message': _("Contact created!")})

        context.update({'form': form})
        return self.return_error(request, context)
