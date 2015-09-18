from apps.contact.models import Contact, ContactSubject


def save(data, user):
    contact = Contact()

    if user.id is None:
        contact.contact_name = data['name']
        contact.contact_email = data['email']
    else:
        contact.author = user

    contact.subject = data['subject']
    contact.message = data['message']

    contact.save()
    return contact


def get_contact_subjects():
    subjects = ContactSubject.objects.all()
    return subjects