from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from apps.community.models import Community
from apps.complaint.models import ComplaintType, Complaint

entity_to_complaint = settings.ENTITY_TO_COMPLAINT if hasattr(settings,
                                        'ENTITY_TO_COMPLAINT') else False


def get_type_complaint():
    complain_type = ComplaintType.objects.all()

    return complain_type

@transaction.atomic
def create_complaint(parameters, user):
    complaint = Complaint()

    content_type = ContentType.objects.get(model=parameters['content_type'])

    complaint.description = parameters['description']
    complaint.complaint_type = parameters['complaint_type']
    complaint.content_type = content_type
    complaint.object_id = parameters['object_id']
    complaint.author = user

    complaint.save()

    for community in parameters['community_complaint']:
        complaint.communities.add(community)

    complaint.save()

    return complaint
