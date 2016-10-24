from django.http import JsonResponse
from django.shortcuts import render
from apps.contact import views
from django.views import View


class CoreContactView(views.ContactView):
    template_path = "contact/partials/contact-form-modal.html"

    render_captcha = False

    def get_context(self):
        context = super(CoreContactView, self).get_context()
        context.update({
            'render_captcha': self.render_captcha
        })
        return context

    def get(self, request):

        if not request.is_ajax():
            self.render_captcha = True
            self.template_path = 'contact/contact-single.html'

        return super(CoreContactView, self).get(request)


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

    def post(self, request):
        if not request.is_ajax():
            self.template_path = 'contact/contact-single.html'
        return super(CoreContactSaveViews, self).post(request)


class CoreContactSuccessView(View):

    template_name = 'contact/contact-success.html'

    def get(self, request):

        return render(request, self.template_name)
