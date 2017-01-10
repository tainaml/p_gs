from django.db import transaction
from apps.company.models import Membership
from apps.core.exceptions.account import NoPermissionToLogWithCompany, CompanyHasNoUserAssociated, NotAllowedToRelogin, \
    UserIdDoesNotRemainsInSession
from apps.userprofile.service import business as BusinessUserProfile
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login as auth_login, get_user_model


@transaction.atomic
def save_profile(user):
    profile = BusinessUserProfile.check_profile_exists(user)
    user.username = str(user.username.lower())
    user.save()
    return profile

#TODO move to Membership Model
def get_permission_to_login(user, company):

    membership = Membership.objects.filter(user=user, company=company)
    if membership:
        return membership[0].permission

    return None


def relogin(request):
    UserModel = get_user_model()
    if request.user.usertype != UserModel.ORGANIZATION:
        raise NotAllowedToRelogin(_("Only company users can relogin"))

    if 'before_user_id' in request.session:
        user_id = request.session['before_user_id']
        user = UserModel.objects.get(id=user_id)

        auth_login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    else:
        raise UserIdDoesNotRemainsInSession(_("Session has no id from user!"))


def log_with_company(request, company):
    permission =Membership.get_permission_to_login(request.user, company)
    if permission:
        user_company = company.user
        before_user_id = request.user.id
        before_user_full_name = request.user.get_full_name()
        before_user_image = request.user.profile.avatar_url

        if user_company:
            auth_login(request, user_company, backend="django.contrib.auth.backends.ModelBackend")
            request.session['before_user_id'] = before_user_id
            request.session['before_user_full_name'] = before_user_full_name
            request.session['before_user_image'] = before_user_image
            request.session['before_user_permission'] = permission
        else:
            raise CompanyHasNoUserAssociated(_("Company has no user associated with"))
    else:
        raise NoPermissionToLogWithCompany(_("User has no permission to log in with this company!"))
