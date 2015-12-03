from django.contrib import admin
from .models import ConfigKey, ConfigValues

admin.site.register(ConfigKey)
admin.site.register(ConfigValues)