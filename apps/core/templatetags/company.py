# coding=utf-8
from apps.core.business.user import User
from apps.company.models import Membership
from django import template

register = template.Library()


@register.inclusion_tag('organization/partials/organization-user-block.html', takes_context=True)
def user_company_block(context, membership_id):

    try:
        membership = Membership.objects.get(id=membership_id)
    except Exception as e:
        return {}

    return {
        'membership': membership
    }