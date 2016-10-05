from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Notification, Alert


class NotificationInline(GenericTabularInline):
    model = Notification

    ct_field = "target_content_type"
    ct_fk_field = "target_object_id"


class AlertAdmin(admin.ModelAdmin):

    inlines = [
        NotificationInline,
    ]


admin.site.register(Notification)
# admin.site.register(Alert, AlertAdmin)
