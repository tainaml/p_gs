from django.db import transaction
from apps.company.models import Membership
from apps.core.exceptions.account import NoPermissionToLogWithCompany, CompanyHasNoUserAssociated
from apps.userprofile.service import business as BusinessUserProfile
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login as auth_login

@transaction.atomic
def save_profile(user):
    profile = BusinessUserProfile.check_profile_exists(user)
    user.username = str(user.username.lower())
    user.save()
    return profile


def get_permission_to_login(user, company):

    membership = Membership.objects.filter(user=user, company=company)
    if membership:
        return membership[0].permission

    return None



def log_with_company(request, company):
    permission = get_permission_to_login(request.user, company)
    if permission:
        user_company = company.user
        if user_company:
            auth_login(request, user_company, backend="django.contrib.auth.backends.ModelBackend")
        else:
            raise CompanyHasNoUserAssociated(_("Company has no user associated with"))
    else:
        raise NoPermissionToLogWithCompany(_("User has no permission to log in with this company!"))
