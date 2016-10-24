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

    def get_context(self):

        subjects = Business.get_contact_subjects()
        context = {
            'subjects': subjects
        }
        return context

    def get(self, request):

        return self.return_success(request, context=self.get_context())


class ContactSaveViews(View):

    template_path = "contact/contact.html"
    form = ContactForm

    render_captcha = False

    def get_context(self, context=None):
        context = {} if context is None else context

        subjects = Business.get_contact_subjects()
        context.update({
            'subjects': subjects,
            'render_captcha': self.render_captcha,
        })
        return context

    def return_error(self, request, context=None):

        if request.is_ajax():
            return JsonResponse({
                'template': render(request, self.template_path, self.get_context(context)).content
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

        if request.is_ajax():
            self.render_captcha = True

        form = self.form(request.user, request.POST)

        context = self.get_context()

        if form.process():
            if request.is_ajax():
                return self.return_success(request, {'message': _("Contact created!")})
            else:
                return redirect(to='contact:success')

        context.update({'form': form})

        if request.is_ajax():
            return self.return_error(request, context)
        else:
            return render(request, template_name=self.template_path, context=context)
