from django.shortcuts import render
from apps.contact.service import business
from apps.contact.service.forms import ContactForm
from django.contrib import messages
from django.utils.translation import ugettext as _


def create(request):
    subjects = business.get_contact_subjects()
    return render(request, 'contact/contact.html', {'subjects': subjects})


def save(request):
    subjects = business.get_contact_subjects()
    form = ContactForm(request.user, request.POST)
    if form.process():
        messages.add_message(
            request,
            messages.SUCCESS,
            _("Contact created!")
        )
    else:
        messages.add_message(
            request,
            messages.WARNING,
            _("Contact not created!")
        )

    return render(request, 'contact/contact.html', {'form': form, 'subjects': subjects})
