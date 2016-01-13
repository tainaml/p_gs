from django.contrib import admin

# Register your models here.
from apps.complaint.models import ComplaintType, Complaint

admin.site.register(ComplaintType)
admin.site.register(Complaint)