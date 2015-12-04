from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import ugettext as _

from ..forms.account import CoreSignUpForm
from apps.account import views

class CoreRegisterView(views.RegisterView):

    form = CoreSignUpForm


class CoreLoginView(views.LoginView):

    def return_error(self, request, context=None):
        _response_context = {}

        if 'form' in context:
            _form = context['form']
            _active = _form.account_is_active if hasattr(_form, 'account_is_active') else None

            _response_context = {
                'errors': _form.errors,
                'is_active': _active
            }

        return JsonResponse(_response_context, status=400)

    def return_success(self, request, context=None):

        return JsonResponse(context, status=200)


class CoreForgotPassword(views.ForgotPasswordView):

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
            'template': render(request, 'account/partials/account-password-response-modal.html', context).content
        }

        return JsonResponse(_context, status=200)


class CoreChangePassword(views.ChangePasswordView):

    def return_error(self, request, context=None):
        _context = {}

        if 'form' in context:
            _form = context['form']
            _context = {'errors': _form.errors}

        return JsonResponse(_context, status=400)

    def return_success(self, request, context=None):
        if not context:
            context = {}

        context.update({
            'title': _('Change Password'),
            'message': _('Your password has been changed!')
        })

        _context = {
            'template': render(request, 'configuration/partials/modal/change-password-successfully.html', context).content
        }

        return JsonResponse(_context, status=200)