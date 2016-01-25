from django.http import JsonResponse
from django.shortcuts import render

from apps.contact import views


class CoreContactView(views.ContactView):
    template_path = "contact/partials/contact-form-modal.html"


class CoreContactSaveViews(views.ContactSaveViews):
    template_path = "contact/partials/contact-form-modal.html"

    def return_error(self, request, context=None):
        response_data = {}

        if 'form' in context:
            response_data.update({'errors': context['form'].errors})

        return JsonResponse(response_data, status=400)

    def return_success(self, request, context=None):
        if not context:
            context = {}

        response_data = {
            'template': render(request, 'contact/partials/contact-response.html', context).content,
            'message': context.get('message')
        }

        return JsonResponse(response_data, status=200)
