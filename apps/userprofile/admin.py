from django.contrib import admin

from apps.userprofile.models import Responsibility, UserProfile

admin.site.register(Responsibility)
admin.site.register(UserProfile)