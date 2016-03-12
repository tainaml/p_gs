from django.contrib import admin

from .models import Contact, ContactSubject

admin.site.register(Contact)
admin.site.register(ContactSubject)
