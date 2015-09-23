from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from apps.complaint.models import ComplaintType, Complaint

entity_to_complaint = settings.ENTITY_TO_COMPLAINT if hasattr(settings,
                                        'ENTITY_TO_COMPLAINT') else False


def get_type_complaint():
    complain_type = ComplaintType.objects.all()

    return complain_type


def create_complaint(parameters, user):
    complaint = Complaint()

    content_type = ContentType.objects.get(model=parameters['content_type'])
    content_object = content_type.get_object_for_this_type(pk=parameters['object_id'])


    complaint.description = parameters['description']
    complaint.complaint_type = parameters['complaint_type']
    complaint.content_type = content_type
    complaint.object_id = parameters['object_id']
    complaint.content_object = content_object
    complaint.author = user

    complaint = complaint.save()

    return complaint
