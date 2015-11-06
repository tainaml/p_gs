from django.http import JsonResponse
from django.shortcuts import render, redirect

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