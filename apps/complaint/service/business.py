from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from apps.complaint.models import ComplaintType, Complaint

entity_to_complaint = settings.ENTITY_TO_COMPLAINT if hasattr(settings,
                                        'ENTITY_TO_COMPLAINT') else False


def get_type_complaint():
    complain_type = ComplaintType.objects.all().order_by('order')

    return complain_type

@transaction.atomic
def create_complaint(parameters, user):

    content_type = ContentType.objects.get(model=parameters['content_type'])

    complaint, created = Complaint.objects.get_or_create(
        description=parameters['description'],
        complaint_type=parameters['complaint_type'],
        content_type=content_type,
        object_id=parameters['object_id'],
        author=user
    )

    for community in parameters['community_complaint']:
        complaint.communities.add(community)

    complaint.save()

    return complaint
