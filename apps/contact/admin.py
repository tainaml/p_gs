from django.contrib import admin
from .models import Contact, ContactSubject
from .service.forms import ContactAdminForm


class ContactAdmin(admin.ModelAdmin):

    form = ContactAdminForm


admin.site.register(Contact, ContactAdmin)
admin.site.register(ContactSubject)
