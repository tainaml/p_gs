from django.contrib import admin

# Register your models here.
from apps.core.models.tags import Tags

admin.site.register(Tags)