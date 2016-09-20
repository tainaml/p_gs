from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django import template
from django.http import Http404

from apps.complaint.service import business
from apps.core.business.content_types import ContentTypeCached

register = template.Library()


@register.inclusion_tag('complaint/report.html', takes_context=True)
def box_complaint(context, content_object, communities):

    try:
        type_complaint = business.get_type_complaint()
        content_type = ContentTypeCached.objects.get_for_model(model=content_object)
        community_complaint = settings.COMPLAINT_COMMUNITY
    except:
        raise Http404()

    return {
        'content_object': content_object,
        'content_type': content_type,
        'request': context['request'],
        'type_complaint': type_complaint,
        'communities': communities,
        'community_complaint': community_complaint
    }