from django.http import JsonResponse
from django.shortcuts import render
from apps.contact import views


class CoreContactView(views.ContactView):
    template_path = "contact/partials/contact-form-modal.html"


class CoreContactSaveViews(views.ContactSaveViews):
    template_path = "contact/partials/contact-form-modal.html"

    def return_error(self, request, context=None):
        _context = {}

        if 'form' in context:
            _form = context['form']
            _context = {'errors': _form.errors}

        return JsonResponse(_context, status=400)

    def return_success(self, request, context=None):

        if not context:
            context = {}

        _context = {
            'template': render(request, 'contact/partials/contact-response.html', context).content,
            'message': context.get('message')
        }

        return JsonResponse(_context, status=200)
