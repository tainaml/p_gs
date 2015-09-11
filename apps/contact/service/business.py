from apps.contact.models import Contact


def save(data, user):
    contact = Contact()

    if user.id is None:
        contact.name = data['name']
        contact.email = data['email']
    else:
        contact.author = user

    contact.subject = data['subject']
    contact.message = data['message']


    contact.save()
    return contact
