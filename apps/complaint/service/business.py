from django.conf import settings
from apps.complaint.models import ComplaintType

entity_to_complaint = settings.ENTITY_TO_COMPLAINT if hasattr(settings,
                                        'ENTITY_TO_COMPLAINT') else False


def get_type_complaint():
    complain_type = ComplaintType.objects.all()

    return complain_type
