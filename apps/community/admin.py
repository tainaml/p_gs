from django.contrib import admin

from .models import Community


class CommunityAdmin(admin.ModelAdmin):
    filter_horizontal = ['related']
    ordering = ['title']

admin.site.register(Community, CommunityAdmin)
