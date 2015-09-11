from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.contact.service.forms import ContactForm
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _


def create(request):
    return render(request, 'contact/contact.html')


def save(request):
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


    return render(request, 'contact/contact.html', {'form': form})
