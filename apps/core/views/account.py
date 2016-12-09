from django.contrib.auth import get_user_model
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from apps.account import views
from apps.company.models import Company
from apps.core.business.account import log_with_company, relogin
from apps.core.exceptions.account import CompanyHasNoUserAssociated, NoPermissionToLogWithCompany, NotAllowedToRelogin, \
    UserIdDoesNotRemainsInSession


class CoreRegisterView(views.RegisterView):

    def redirect_to(self, request):
        return redirect(reverse('profile:feed'))


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


class LoginWithCompany(views.View):

    @method_decorator(login_required)
    def get(self,request, company_slug):

        try:
            company = Company.objects.get(user__username=company_slug)
            if company.user == request.user:
                return redirect(reverse('profile:feed'))

            log_with_company(request, company)
            return redirect(reverse('profile:feed'))
        except (Company.DoesNotExist, CompanyHasNoUserAssociated, NoPermissionToLogWithCompany):
            raise Http404()

class ReLoginFromCompany(views.View):

    @method_decorator(login_required)
    def get(self,request):
        UserModel = get_user_model()
        try:

            relogin(request)
            return redirect(reverse('profile:feed'))
        except (UserModel.DoesNotExist, NotAllowedToRelogin, UserIdDoesNotRemainsInSession):
            return redirect(reverse('account:logout'))



class CoreResendAccountConfirmationView(views.ResendAccountConfirmationView):

    def return_error(self, request, context=None):
        _response_context = {}

        if 'form' in context:
            _form = context['form']

            _response_context = {
                'errors': _form.errors
            }

        return JsonResponse(_response_context, status=400)

    def return_success(self, request, context=None):
        context.update({
            'title': _('Resend confirmation email'),
            'message': _('E-mail re-sent successfully!')
        })

        response_data = {
            'template': render(request, 'account/partials/account-modal-message.html', context).content
        }
        return JsonResponse(response_data, status=200)


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
