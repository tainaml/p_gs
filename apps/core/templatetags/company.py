# coding=utf-8
from apps.core.business.user import User
from apps.company.models import Membership
from django import template

register = template.Library()


@register.inclusion_tag('organization/partials/organization-user-block.html', takes_context=True)
def user_company_block(context, user_id, permission):

    default_permission_name = Membership.MEMBERSHIP_TYPES.get(Membership.COLLABORATOR)
    permission_name = Membership.MEMBERSHIP_TYPES.get(int(permission), default_permission_name)

    try:
        user = User.objects.get(id=user_id)

    except Exception as e:
        return {}

    return {
        'user': user,
        'permission_name': permission_name
    }